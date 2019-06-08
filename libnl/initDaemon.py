import daemon
import sys
import os
import subprocess
# Client side : from multiprocessing.connection import Client
# Listener side : from multiprocessing.connection import Listener
from daemon import pidfile


# socket creation
def procedure():
	"""
	# client side
        # 7000 port number
	addr = ('localhost', 7000)
	connection = Client(addr, authkey='secret')
        ... start communication

	# listener side
        addr = ('localhost', 7000)
        connection = Listener(addr, authKey='secret')
	listener.accept()
        ... listen to client side
	while True:
		msg = connection.recv()
		# close socket
                if msg == 'close':
			connection.close()
			break

	"""
        #Put [PATH TO scanAPs.py] according to yours
	print(subprocess.check_output("python [PATH TO scanAPs.py] -n wlp2s0", shell=True).decode('utf-8'))

def start_daemon():
	with daemon.DaemonContext(
		stdout = sys.stdout,
		stderr = sys.stderr) as context:
		procedure()

if __name__ == "__main__":
	start_daemon()
