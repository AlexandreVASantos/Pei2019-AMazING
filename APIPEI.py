from flask import Flask, request, json
from flask_restful import Api, Resource, reqparse
import subprocess

app = Flask(__name__)
api = Api(app)
flagAP=0

@app.route("/")
def hello():
	return "root API amazing PEI \n"


class connection(Resource):
	def post(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			global flagAP
			args=request.get_json()		
			if(len(args) == 3):
				SSID = args.get('SSID')
				PASS = args.get('PASS')
				NetwC = args.get('NetwC')
				if(flagAP==1 and NetwC=="wlp5s0"):
					out = json.dumps({'Message': 'wlp5s0 is being used as an access point'})
					return out
				command = "wpa_passphrase " + SSID + " " + PASS + " | sudo tee /etc/wpa_supplicant.conf"
				out = subprocess.check_output(command, shell=True)
				command2 = "sudo wpa_supplicant -B -c /etc/wpa_supplicant.conf -i " + NetwC
				out = out + subprocess.check_output(command2, shell=True)
				command3 = "sudo dhclient -v " + NetwC
				out = out + subprocess.check_output(command3, shell=True)
				out = out.decode("utf-8")
			else:
				out = json.dumps({'Message': 'Incorrect arg number, needs to be 3'})
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e)

class disconnect(Resource):
	def get(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)		
			out = subprocess.check_output("sudo killall wpa_supplicant", shell=True)
			out = out + subprocess.check_output("sudo killall dhclient", shell=True)
			out = out.decode("utf-8") 
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))

class postGetApIP(Resource):
	def get(self):
		if(flagAP==1):
			try:
				out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
				out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)		
				out = subprocess.check_output("cat /var/lib/misc/dnsmasq.leases", shell=True)
				out = out.decode("utf-8") 
				return out
			except subprocess.CalledProcessError as e:
				return json.dumps(e.output.decode("utf-8"))
		else:
			out = json.dumps({'Message': 'There is no AccessPoint activated'})

class changeIP(Resource):
	def post(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			args=request.get_json()
			IP = args.get('IP')
			NetwC = args.get('NetwC')
			Netmask = args.get('Netmask')
			if(len(args) == 3):
				command = "sudo ifconfig " + NetwC + " " + IP + " netmask " + Netmask
				out = subprocess.check_output(command, shell=True)
				out = out.decode("utf-8")
			else:
				out = json.dumps({'Message': 'Incorrect arg number, needs to be 2'})
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))

class getifconfig(Resource):
	def post(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			args = request.get_json()
			NetwC = args.get('NetwC')
			if(len(args) == 1):
				out = subprocess.check_output("sudo ifconfig | grep -m1 '" + NetwC + "' -A 1", shell=True)
				out = out.decode("utf-8")
			else:
				out = json.dumps({'Message': 'Incorrect arg number, needs to be 1'})
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))	

class getlist(Resource):
	def get(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			out = subprocess.check_output("iw list", shell=True)
			out = out.decode("utf-8")
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))

class CreateAccessPoint(Resource):
	def post(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			global flagAP
			if(flagAP==1):
				out = json.dumps({'Message': 'AccessPoint already active'})
				out = out.decode("utf-8")
				return out
			args=request.get_json()
			APSSID = args.get('APSSID')
			APPW = args.get('APPW')
			Channel = args.get('Channel')
			RangeStart = args.get('RangeStart')
			RangeEnd = args.get('RangeEnd')
			hw_mode = args.get('hw_mode')
			DFGateway = args.get('DFGateway')
			Netmask = args.get('Netmask')
			out = subprocess.check_output('printf "interface=wlp5s0\ndriver=nl80211\nssid=' + APSSID + '\nhw_mode=' + hw_mode + '\nchannel='+ Channel + '\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=3\nwpa_passphrase=' + APPW + '\nwpa_key_mgmt=WPA-PSK\nwpa_pairwise=TKIP\nrsn_pairwise=CCMP\n"  > /etc/hostapd/hostapd.conf', shell=True)
			out = subprocess.check_output('printf "interface=wlp5s0\ndhcp-range=' + RangeStart + ',' + RangeEnd + ',' + Netmask + ',12h\ndhcp-option=3\ndhcp-option=6" > /etc/dnsmasq.conf', shell=True)
			out = subprocess.check_output('sysctl -w net.ipv4.ip_forward=1', shell=True)
			out = subprocess.check_output("sudo ifconfig wlp5s0 " + DFGateway + " netmask " + Netmask, shell=True)
			out = subprocess.check_output("sudo hostapd -B /etc/hostapd/hostapd.conf", shell=True)		
			out = subprocess.check_output("sudo /etc/init.d/dnsmasq restart", shell=True)
			out = out.decode("utf-8")
			flagAP=1
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))

class StopAccessPoint(Resource):
	def get(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			global flagAP
			if(flagAP == 1):
				out = subprocess.check_output("sudo service dnsmasq stop", shell=True)
				out = subprocess.check_output("sudo killall hostapd", shell=True)
				out = out.decode("utf-8")
				flagAP=0
				return out
			else:
				out = json.dumps({'Message':'There is no AccessPoint to stop.'})
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))		


class scan(Resource):
	def post(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			args = request.get_json()
			NetwC = args.get('NetwC')
			if(len(args) == 1):
				out = subprocess.check_output("sudo iw dev " + NetwC + " scan", shell=True)
				out = out.decode("utf-8")
			else:
				out = json.dumps({'Message': 'Incorrect args, needs to receive the NetworkCard'})
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))

class localwireless(Resource):
	def post(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			args = request.get_json()
			NetwC = args.get('NetwC')
			if(len(args) == 1):
				out = subprocess.check_output("sudo ifconfig " + NetwC + " up", shell=True)
				out = subprocess.check_output("sudo iw " + NetwC + " scan | grep 'SSID\|freq\|signal'", shell=True)
				out = out.decode("utf-8")
			else:
				out = json.dumps({'Message': 'Incorrect args, needs to receive the NetworkCard'})
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))
	
class link(Resource):
	def post(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			args = request.get_json()
			NetwC = args.get('NetwC')
			if(len(args) == 1):
				out = subprocess.check_output("iw dev " + NetwC + " link", shell=True)
				out = out.decode("utf-8")
			else:
				out = json.dumps({'Message': 'Incorrect args, needs to receive the NetworkCard'})
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))

class stationstats(Resource):
	def post(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			args = request.get_json()
			NetwC = args.get('NetwC')
			if(len(args) == 1):
				out = subprocess.check_output("iw dev " + NetwC + " station dump", shell=True)
				out = out.decode("utf-8")
			else:
				out = json.dumps({'Message': 'Incorrect args, needs to receive the NetworkCard'})
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))


class stationpeerstats(Resource):
	def get(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			args=request.get_json()
			NetwC = args.get('NetwC')
			MAC = args.get('MAC')
			if(len(args) == 2):
				out = subprocess.check_output("sudo iw dev " + NetwC + " station get " + MAC, shell=True)
				out = out.decode("utf-8")
			else:
				out = json.dumps({'Message': 'Incorrect args, needs to receive the NetworkCard'})
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))
		
class modtxhtmcsbitrates(Resource):
	def post(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			args = request.get_json()
			NetwC = args.get('NetwC')
			Lbits = args.get('Lbits')
			if(len(args) == 1):
				out = subprocess.check_output("iw " + NetwC + " set bitrates " + Lbits, shell=True)
				out = out.decode("utf-8")
			else:
				out = json.dumps({'Message': 'Incorrect args, needs to receive the NetworkCard and the bits'})
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))

class settingtxpowerdev(Resource):
	def post(self):
		try:
			out = subprocess.check_output("ifconfig wlp1s0 up ", shell=True)
			out = subprocess.check_output("ifconfig wlp5s0 up ", shell=True)
			args = request.get_json()
			NetwC = args.get('NetwC')
			Type = args.get('Type')
			Power = args.get('Power')
			if(len(args) == 1):
				out = subprocess.check_output("iw dev " + NetwC + " " + Type + " " + Power, shell=True)
				out = out.decode("utf-8")
			else:
				out = json.dumps({'Message': 'Incorrect args, needs to receive the NetworkCard'})
			return out
		except subprocess.CalledProcessError as e:
			return json.dumps(e.output.decode("utf-8"))

api.add_resource(connection, '/connection')					#POST e GET
api.add_resource(disconnect, '/disconnect')					#GET
api.add_resource(postGetApIP, '/postGetApIP')				#GET
api.add_resource(changeIP, '/changeIP')						#POST e GET
api.add_resource(getifconfig,'/getifconfig')				#POST
api.add_resource(getlist, '/getlist')						#GET
api.add_resource(CreateAccessPoint, '/CreateAccessPoint')	#POST
api.add_resource(StopAccessPoint, '/StopAccessPoint')		#GET
api.add_resource(scan,'/scan')								#POST
api.add_resource(localwireless,'/localwireless')			#POST
api.add_resource(link,'/link')								#POST
api.add_resource(stationstats,'/stationstats')				#POST
api.add_resource(stationpeerstats, '/stationpeerstats')		#POST
api.add_resource(modtxhtmcsbitrates,'/modtxhtmcsbitrates')	#POST
api.add_resource(settingtxpowerdev,'/settingtxpowerdev')	#POST

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')