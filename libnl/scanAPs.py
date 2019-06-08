import socket
import sys
import os
import signal
import ctypes
import time

#conversions between Python values and C structs
#handle binary data stored from network communications
import struct

#usage-messages, docstrings by me
from docopt import docopt
from terminaltables import AsciiTable

args = docopt("""
Usage:
    example_show_wifi_interface.py [-k COLUMN] [-n] [-r] [-v ...] <interface>
    example_show_wifi_interface.py -h | --help
Options:
    -k --key=COLUMN     Sort table by column name (case insensitive).
                        [default: SSID]
    -n --no-sudo        Don't trigger a scan. Attempt to read previous scan's
                        results. Use this if you use something like
                        `sudo iw dev wlan0 scan` very recently. The kernel may
                        still have the results stored in memory.
    -r --reverse        Reverse the results.
    -v --verbose        Print debug messages to stderr. Specify twice for more.
""")

import libnl.handlers
from libnl.attr import nla_parse, nla_parse_nested, nla_put, nla_put_nested, nla_put_u32
from libnl.error import errmsg
from libnl.genl.ctrl import genl_ctrl_resolve, genl_ctrl_resolve_grp
from libnl.genl.genl import genl_connect, genlmsg_attrdata, genlmsg_attrlen, genlmsg_put
from libnl.linux_private.genetlink import genlmsghdr
from libnl.linux_private.netlink import NLM_F_DUMP,  NLM_F_DUMP_INTR
from libnl.msg import nlmsg_alloc, nlmsg_data, nlmsg_hdr
from libnl.nl import nl_recvmsgs, nl_send_auto, nl_complete_msg, nl_send
from libnl.nl80211 import nl80211
from libnl.nl80211.helpers import parse_bss
from libnl.nl80211.iw_scan import bss_policy
from libnl.socket_ import nl_socket_add_membership, nl_socket_alloc, nl_socket_drop_membership

COLUMNS = ['SSID', 'Channel', 'Frequency', 'Signal', 'BSSID']

NL_AUTO_PORT = 0
NL_AUTO_SEQ = 0

def main():
	
	try:
		if_index = socket.if_nametoindex(args['<interface>'])
	except OSError:
		return error('Wireless interface {0} does not exist.'.format(args['<interface>']))

	#open a socket to kernel
	sk = nl_socket_alloc()
	#create a file descriptor and bind socket
	success = genl_connect(sk)
	#nl80211 driver ID
	driverID = genl_ctrl_resolve(sk, b'nl80211')
	if driverID < 0:
		return error('Invalid family identifier, return {0}'.format(driverID))

	#group in nl80211 family, scan
	group = genl_ctrl_resolve_grp(sk, b'nl80211', b'scan')
	if group < 0:
		return error('Invalid group identifier, return {0}'.format(group))

	results = dict()

	for i in range(0,3):
		if not args['--no-sudo']:
			ret = requestAndSignals(sk, if_index, driverID, group)
			if ret < 0:
				time.sleep(5)
				continue
		ret = resultHandler(sk, if_index, driverID, results)
		if ret < 0:
			time.sleep(5)
			continue
		break

	if not results:
		print('No access points detected.')
		return

	# Print results.
	print('Found {0} access points:'.format(len(results)))
	printTable(results.values())

def requestAndSignals(socket,if_index, driverID, group):	
	# listen results for scan requests 
	success = nl_socket_add_membership(socket, group)
	if success < 0:
		return success

	# msg to kernel
	msg = nlmsg_alloc()
	genlmsg_put(msg, 0, 0, driverID, 0, 0, nl80211.NL80211_CMD_TRIGGER_SCAN, 0) # Command to run
	nla_put_u32(msg, nl80211.NL80211_ATTR_IFINDEX, if_index) # interface
	scan_parameters = nlmsg_alloc()
	nla_put(scan_parameters, 1, 0, b'') # scan ssids
	nla_put_nested(msg, nl80211.NL80211_ATTR_SCAN_SSIDS, scan_parameters) # scan type

	# signal values
	signalMsg = ctypes.c_int(1)
	results = ctypes.c_int(-1)
	# setup proper callbacks
	callbackHandle = libnl.handlers.nl_cb_alloc(libnl.handlers.NL_CB_DEFAULT)
	libnl.handlers.nl_cb_set(callbackHandle, libnl.handlers.NL_CB_VALID, libnl.handlers.NL_CB_CUSTOM, scanSuccessful, results)
	libnl.handlers.nl_cb_err(callbackHandle, libnl.handlers.NL_CB_CUSTOM, errorHandler, signalMsg)
	libnl.handlers.nl_cb_set(callbackHandle, libnl.handlers.NL_CB_ACK, libnl.handlers.NL_CB_CUSTOM, ackHandler, signalMsg)
	libnl.handlers.nl_cb_set(callbackHandle, libnl.handlers.NL_CB_SEQ_CHECK, libnl.handlers.NL_CB_CUSTOM, lambda *_ : libnl.handlers.NL_OK, None)

	# send message to kernel
	success = nl_send_auto(socket, msg)
	if success < 0:
		return success
	while signalMsg.value > 0:
		success = nl_recvmsgs(socket, callbackHandle)
		if success < 0:
			return success
	if signalMsg.value < 0:
		error('Unknown error {0} ({1})'.format(signalMsg.value, errmsg[abs(signalMsg.value)]))

	# Block while operation is not complete
	while results.value < 0:
		success = nl_recvmsgs(socket, callbackHandle)
		if success < 0:
			return success

	if results.value > 0:
		error('Scan aborted')

	return nl_socket_drop_membership(socket, group)

def resultHandler(socket, if_index, driverID, results):
	msg =nlmsg_alloc()
	#NLM_F_DUMP
	genlmsg_put(msg, NL_AUTO_PORT, NL_AUTO_SEQ, driverID, 0, NLM_F_DUMP, nl80211.NL80211_CMD_GET_SCAN, 0)
	nla_put_u32(msg, nl80211.NL80211_ATTR_IFINDEX, if_index)
	callbackHandle = libnl.handlers.nl_cb_alloc(libnl.handlers.NL_CB_DEFAULT)
	libnl.handlers.nl_cb_set(callbackHandle, libnl.handlers.NL_CB_VALID, libnl.handlers.NL_CB_CUSTOM, decodeInfo, results)
	nl_complete_msg(socket, msg)
	success = nl_send(socket, msg)

	if success >= 0:
		success = nl_recvmsgs(socket, callbackHandle)

	return success

def scanSuccessful(msg, n):
	gnlh = genlmsghdr(nlmsg_data(nlmsg_hdr(msg)))
	if gnlh.cmd == nl80211.NL80211_CMD_SCAN_ABORTED:
		n.value = 1
	elif gnlh.cmd == nl80211.NL80211_CMD_NEW_SCAN_RESULTS:
		n.value = 0
	return libnl.handlers.NL_SKIP

def decodeInfo(msg, results):
	bss = dict()

	# Parse information
	gnlh = genlmsghdr(nlmsg_data(nlmsg_hdr(msg)))
	tb = dict((i, None) for i in range(nl80211.NL80211_ATTR_MAX + 1))
	nla_parse(tb, nl80211.NL80211_ATTR_MAX, genlmsg_attrdata(gnlh, 0), genlmsg_attrlen(gnlh, 0), None)

	if not tb[nl80211.NL80211_ATTR_BSS]:
		print('WARNING: BSS info missing for an AP.')
		return libnl.handlers.NL_SKIP
	if nla_parse_nested(bss, nl80211.NL80211_BSS_MAX, tb[nl80211.NL80211_ATTR_BSS], bss_policy):
		print('WARNING: Failed to parse nested attributes for an AP.')
		return libnl.handlers.NL_SKIP
	if not bss[nl80211.NL80211_BSS_BSSID]:
		print('WARNING: No BSSID detected for an AP.')
		return libnl.handlers.NL_SKIP
	if not bss[nl80211.NL80211_BSS_INFORMATION_ELEMENTS]:
		print('WARNING: No additional information available for an AP.')
		return libnl.handlers.NL_SKIP

	bss_parsed = parse_bss(bss)
	results[bss_parsed['bssid']] = bss_parsed
	return libnl.handlers.NL_SKIP

def printTable(data):

	table = AsciiTable([COLUMNS])
	table.justify_columns[2]='right'
	table.justify_columns[3]='right'
	table.justify_columns[4]='right'
	tableData = list()

	for row_in in data:
		row_out = [
			str(row_in.get('ssid', '')),
			str(row_in.get('channel', '')),
			str(row_in.get('frequency', '')),
			str(row_in.get('signal', '')),
			str(row_in.get('bssid', '')),
		]
		if row_out[2]:
			row_out[2] += ' Mhz'
		if row_out[3]:
			row_out[3] += ' dBm'
		tableData.append(row_out)

	sortByColumn = [c.lower() for c in COLUMNS].index(args['--key'].lower())
	tableData.sort(key=lambda c: c[sortByColumn], reverse=args['--reverse'])

	table.table_data.extend(tableData)
	print(table.table)

def errorHandler(_, err, n):
	n.value = err.error
	return libnl.handlers.NL_STOP

def ackHandler(_, n):
	n.value = 0	
	return libnl.handlers.NL_STOP

def error(msg):
	if msg:
		print('ERROR : {0}'.format(msg), file=sys.stderr)
	else:
		print(file=sys.stderr)
	sys.exit(1)

if __name__ == '__main__':
	main()