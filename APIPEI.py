from flask import Flask, jsonify, request, json 	#, abort
from flask_restful import Api, Resource, reqparse
import subprocess

# https://wireless.wiki.kernel.org/en/users/documentation/hostapd

app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello():
	return "root API amazing PEI \n"

class connection(Resource):
	def get(self):
		return {'status' : 'estado atual'}

	def post(self):
		# if not request.json or not 'SSID' in request.json:
		#	abort(400)

		args=request.get_json()
		sudo_password = 'JustGetIn666'
		
		if(len(args) == 1):
			# chamar conexão com SSID apenas
			SSID = args.get('SSID')
			command = "sudo iw wlp1s0 connect wsiit" + SSID
			command = command.split()
			cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
			cmd2 = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)
		elif(len(args) == 2):
			#chamar conexão com SSID e Frequência
			SSID = args.get('SSID')
			Freq = args.get('Frequency')
			ree = "iw wlp1s0 connect " + SSID + Freq
		elif(len(args) == 3):
			SSID = args.get('SSID')
			Freq = args.get('Frequency')
			WEP = args.get('WEP')
			ree = "iw wlp1s0 connect " + SSID + Freq + WEP
		else:
			response = jsonify({'Not the right ammount of args': 'needs to be between 1 and 3'})

		# response.status_code = 201
		string =  "iw wlp1s0 connect 1234567890123456789012345679012"

		output = subprocess.run(ree, stdout=subprocess.PIPE, universal_newlines=True)
		return output.stdout
		#return ree

# exemplo: curl -H "Content-Type: application/json"  localhost:5000/connection -X post -d '{"SSID":"foo","Frequency":"1234","WEP":"1234123asdgwer"}'

class changeIP(Resource):
	def get(self):
		out = subprocess.check_output("ifconfig | grep -m1 'inet'", shell=True)
		out = out.decode("utf-8") 
		return out

	def post(self):
		sudo_password = 'JustGetIn666'
		args=request.get_json()
		IP = args.get('IP')
		if(len(args) == 1):
			command = "sudo ifconfig enp2s0 " + IP + " netmask 255.255.255.0"
			command = command.split()
			cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
			cmd2 = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)
			response = cmd2.stdout.read().decode()
		else:
			response = jsonify({'Not the right ammount of args': 'needs to be 1'})
		temp = subprocess.check_output("curl localhost:5000/changeIP", shell=True)
		temp = temp.decode("utf-8")
		return temp

		# exemplo: curl -H "Content-Type: application/json"  localhost:5000/connection -X post -d '{"IP":"192.168.0.16"}'

class getlist(Resource):
	def get(self):
		out = subprocess.check_output("iw list", shell=True)
		out = out.decode("utf-8") 
		return out

# exemplo: curl localhost:5000/getlist

class event(Resource):
	def get(self):
		out = subprocess.check_output("iw event", shell=True)
		out = out.decode("utf-8") 
		return out
# exemplo: curl localhost:5000/event

class eventt(Resource):
	def get(self):
		out = subprocess.check_output("iw event -t", shell=True)
		out = out.decode("utf-8") 
		return out
#exemplo: curl localhost:5000/eventt

class eventf(Resource):
	def get(self):
		out = subprocess.check_output("iw event -f", shell=True)
		out = out.decode("utf-8") 
		return out
#exemplo: curl localhost:5000/eventf

class scan(Resource):
	def get(self):
		sudo_password = 'JustGetIn666'
		command = "sudo iw dev wlp1s0 scan"
		command = command.split()
		cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
		cmd2 = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)
		response = cmd2.stdout.read().decode()
		return response
#exemplo: curl localhost:5000/scan

class localwireless(Resource):
	def get(self):
		out = subprocess.check_output("nmcli dev wifi", shell=True)
		out = out.decode("utf-8") 
		return out
#exemplo: curl localhost:5000/localwireless

class link(Resource):
	def get(self):
		out = subprocess.check_output("iw dev wlp1s0 link", shell=True)
		out = out.decode("utf-8") 
		return out
#exemplo: curl localhost:5000/link

class stationstats(Resource):
	def get(self):
		out = subprocess.check_output("iw dev wlp1s0 station dump", shell=True)
		out = out.decode("utf-8") 
		return out
#exemplo: curl localhost:5000/stationstats

class stationpeerstats(Resource):
	def get(self):
		sudo_password = 'JustGetIn666'
		args=request.get_json()
		MAC = args.get('MAC')
		if(len(args) == 1):
			command = "sudo iw dev wlp1s0 station get " + MAC
			command = command.split()
			cmd1 = subprocess.Popen(['echo',sudo_password], stdout=subprocess.PIPE)
			cmd2 = subprocess.Popen(['sudo','-S'] + command, stdin=cmd1.stdout, stdout=subprocess.PIPE)
			response = cmd2.stdout.read().decode()
		else:
			response = jsonify({'Not the right ammount of args': 'needs to be 1'})
		return response
		
# exemplo: curl -H "Content-Type: application/json"  localhost:5000/stationpeerstats -X post -d '{"MAC":"<mac-address>"}'

class modlegacytxbitrates(Resource):
	def post(self):
		# args=request.get_json()
		response = jsonify('implementada alteração com $ iw wlan0 set bitrates legacy-2.4 x y z')
		return response

# exemplo: curl -H "Content-Type: application/json"  localhost:5000/modlegacytxbitrates -X post -d '{"x":"1","y":"2","z":"3"}'

class modtxhtmcsbitrates(Resource):
	def post(self):
		# args=request.get_json()
		response = jsonify('implementada alteração com $ iw dev wlan0 set bitrates mcs-5 4 (ou mcs-2.4 10)')
		return response
# exemplo: curl -H "Content-Type: application/json"  localhost:5000/modtxhtmcsbitrates -X post -d '{"mcs":"numeros"}'

class settingtxpowerdev(Resource):
	def post(self):
		# args=request.get_json()
		response = jsonify('implementada alteração com $ iw dev <devname> set txpower <auto|fixed|limit> [<tx power in mBm>]')
		return response
# exemplo: curl -H "Content-Type: application/json"  localhost:5000/settingtxpowerdev -X post -d '{"mcs":"numeros"}'


#class settingtxpowerphy(Resource):
#	def post(self):
		# args=request.get_json()
#		response = jsonify('implementada alteração com $ iw phy <phyname> set txpower <auto|fixed|limit> [<tx power in mBm>]')
#		return response
# exemplo: curl -H "Content-Type: application/json"  localhost:5000/settingtxpowerphy -X post -d '{"mcs":"numeros"}'

api.add_resource(connection, '/connection')					#POST e GET
api.add_resource(changeIP, '/changeIP')						#POST e GET
api.add_resource(getlist, '/getlist')						#GET
api.add_resource(event, '/event')							#GET
api.add_resource(eventt,'/eventt')							#GET
api.add_resource(eventf,'/eventf')							#GET
api.add_resource(scan,'/scan')								#GET
api.add_resource(localwireless,'/localwireless')			#GET
api.add_resource(link,'/link')								#GET
api.add_resource(stationstats,'/stationstats')				#GET
api.add_resource(stationpeerstats, '/stationpeerstats')		#POST
api.add_resource(modlegacytxbitrates,'/modlegacytxbitrates')#POST
api.add_resource(modtxhtmcsbitrates,'/modtxhtmcsbitrates')	#POST
api.add_resource(settingtxpowerdev,'/settingtxpowerdev')	#POST
# api.add_resource(settingtxpowerphy,'/settingtxpowerphy')	#POST




if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')