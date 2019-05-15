from flask import Flask, jsonify, request, json
from flask_restful import Api, Resource, reqparse
import subprocess

# https://wireless.wiki.kernel.org/en/users/documentation/hostapd

app = Flask(__name__)
api = Api(app)
flag=0

@app.route("/")
def hello():
	return "root API amazing PEI \n"

class connection(Resource):
	def post(self):
		args=request.get_json()		
		if(len(args) == 3):
			SSID = args.get('SSID')
			PASS = args.get('PASS')
			NetwC = args.get('NetwC')
			command = "wpa_passphrase " + SSID + " " + PASS + " | sudo tee /etc/wpa_supplicant.conf"
			out = subprocess.check_output(command, shell=True)
			command2 = "sudo wpa_supplicant -B -c /etc/wpa_supplicant.conf -i " + NetwC
			out = out + subprocess.check_output(command2, shell=True)
			command3 = "sudo dhclient " + NetwC
			out = out + subprocess.check_output(command3, shell=True)
			out = out.decode("utf-8")
		else:
			out = jsonify({'Not the right ammount of args': 'needs to be 3 or 4'})
		return out

#curl -H "Content-Type: application/json"  localhost:5000/connection -X post -d '{"NetwC":"wlp1s0","SSID":"IoT-privacy","PASS":"deadpool2"}'


class disconnection(Resource):
	def get(self):
		out = subprocess.check_output("sudo killall wpa_supplicant", shell=True)
		out = out + subprocess.check_output("sudo killall dhclient", shell=True)
		out = out.decode("utf-8") 
		return out


class changeIP(Resource):
	def post(self):
		args=request.get_json()
		IP = args.get('IP')
		NetwC = args.get('NetwC')
		if(len(args) == 2):
			command = "sudo ifconfig " + NetwC + " " + IP + " netmask 255.255.255.0"
			out = subprocess.check_output(command, shell=True)
			out = out.decode("utf-8")
		else:
			out = jsonify({'Not the right ammount of args': 'needs to be 2'})
		out = subprocess.check_output("curl localhost:5000/changeIP", shell=True)
		out = out.decode("utf-8")
		return out

		# exemplo: curl -H "Content-Type: application/json"  localhost:5000/connection -X post -d '{"IP":"192.168.0.16"}'

class getifconfig(Resource):
	def post(self):
		args = request.get_json()
		NetwC = args.get('NetwC')
		if(len(args) == 1):
			out = subprocess.check_output("sudo ifconfig | grep -m1 '" + NetwC + "' -A 1", shell=True)
			out = out.decode("utf-8")
		else:
			out = jsonify({"Incorret args": 'needs to be 1'})
		return out


class getlist(Resource):
	def get(self):
		out = subprocess.check_output("iw list", shell=True)
		out = out.decode("utf-8")
		return out

# exemplo: curl localhost:5000/getlist

class CreateAcessPoint(Resource):
	def post(self):
		args=request.get_json()
		out = "null"
		return out

class event(Resource):
	def post(self):
		args=request.get_json()
		option = args.get('option')
		if(len(args) == 1):
			if(option==1):
				out = subprocess.check_output("iw event", shell=True)
				out = out.decode("utf-8")
			elif(option==2):
				out = subprocess.check_output("iw event -t", shell=True)
				out = out.decode("utf-8")
			elif(option==3):
				out = subprocess.check_output("iw event -f", shell=True)
				out = out.decode("utf-8")
			else:
				out = jsonify({"Incorret option": 'needs to be 1-3'})
		else:
			out = jsonify({"Incorret args": 'needs to be 1'})

		return out
# exemplo: curl localhost:5000/event

class scan(Resource):
	def post(self):
		args = request.get_json()
		NetwC = args.get('NetwC')
		if(len(args) == 1):
			out = subprocess.check_output("sudo iw dev'" + NetwC + "' scan", shell=True)
			out = out.decode("utf-8")
		else:
			out = jsonify({'Not the right ammount of args': 'needs to receive NetworkCard'})
		return out
#exemplo: curl localhost:5000/scan

class localwireless(Resource):
	def post(self):
		args = request.get_json()
		NetwC = args.get('NetwC')
		if(len(args) == 1):
			out = subprocess.check_output("sudo iw " + NetwC + " scan | grep 'SSID\|freq\|signal'", shell=True)
			out = out.decode("utf-8")
		else:
			out = jsonify({'Not the right ammount of args': 'needs to receive NetworkCard'})
		return out
		# exemplo: curl -H "Content-Type: application/json"  localhost:5000/localwireless -X post -d '{"NetwC":"wlp1s0"}'
	
class link(Resource):
	def post(self):
		args = request.get_json()
		NetwC = args.get('NetwC')
		if(len(args) == 1):
			out = subprocess.check_output("iw dev " + NetwC + " link", shell=True)
			out = out.decode("utf-8")
		else:
			out = jsonify({'Not the right ammount of args': 'needs to receive NetworkCard'})
		return out
#exemplo: curl localhost:5000/link

class stationstats(Resource):
	def post(self):
		args = request.get_json()
		NetwC = args.get('NetwC')
		if(len(args) == 1):
			out = subprocess.check_output("iw dev " + NetwC + " station dump", shell=True)
			out = out.decode("utf-8")
		else:
			out = jsonify({'Not the right ammount of args': 'needs to receive NetworkCard'})
		return out
#exemplo: curl localhost:5000/stationstats

class stationpeerstats(Resource):
	def get(self):
		args=request.get_json()
		NetwC = args.get('NetwC')
		MAC = args.get('MAC')
		if(len(args) == 2):
			out = subprocess.check_output("sudo iw dev " + NetwC + " station get " + MAC, shell=True)
			out = out.decode("utf-8")
		else:
			out = jsonify({'Not the right ammount of args': 'needs to receive NetworkCard'})
		return out
		
# exemplo: curl -H "Content-Type: application/json"  localhost:5000/stationpeerstats -X post -d '{"MAC":"<mac-address>"}'

class modtxhtmcsbitrates(Resource):
	def post(self):
		args = request.get_json()
		NetwC = args.get('NetwC')
		Lbits = args.get('Lbits')
		if(len(args) == 1):
			out = subprocess.check_output("iw " + NetwC + " set bitrates " + Lbits, shell=True)
			out = out.decode("utf-8")
		else:
			out = jsonify({"Not the right ammount of args": 'needs to receive NetworkCard and Lbits'})
		return out
# exemplo: curl -H "Content-Type: application/json"  localhost:5000/modtxhtmcsbitrates -X post -d '{"mcs":"numeros"}'

class settingtxpowerdev(Resource):
	def post(self):
		args = request.get_json()
		NetwC = args.get('NetwC')
		Type = args.get('Type')
		Power = args.get('Power')
		if(len(args) == 1):
			out = subprocess.check_output("iw dev " + NetwC + " " + Type + " " + Power, shell=True)
			out = out.decode("utf-8")
		else:
			out = jsonify({'Not the right ammount of args': 'needs to receive NetworkCard'})
		return out
# exemplo: curl -H "Content-Type: application/json"  localhost:5000/settingtxpowerdev -X post -d '{"mcs":"numeros"}'


api.add_resource(connection, '/connection')					#POST e GET
api.add_resource(disconnection, '/disconnection')			#GET
api.add_resource(changeIP, '/changeIP')						#POST e GET
api.add_resource(getifconfig,'/getifconfig')				#POST
api.add_resource(getlist, '/getlist')						#GET
api.add_resource(CreateAcessPoint, '/CreateAcessPoint')		#POST
api.add_resource(event, '/event')							#POST
api.add_resource(scan,'/scan')								#POST
api.add_resource(localwireless,'/localwireless')			#POST
api.add_resource(link,'/link')								#POST
api.add_resource(stationstats,'/stationstats')				#POST
api.add_resource(stationpeerstats, '/stationpeerstats')		#POST
api.add_resource(modtxhtmcsbitrates,'/modtxhtmcsbitrates')	#POST
api.add_resource(settingtxpowerdev,'/settingtxpowerdev')	#POST

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')