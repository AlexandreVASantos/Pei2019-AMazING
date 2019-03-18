from flask import Flask, jsonify, request, json 	#, abort
from flask_restful import Api, Resource, reqparse

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

		if(len(args) == 1):
			# chamar conexão com SSID apenas
			response = jsonify(args)
		elif(len(args) == 2):
			#chamar conexão com SSID e Frequência
			response = jsonify(args)
		elif(len(args) == 3):
			#chamar conexão com SSID, Frequência e WEP
			response = jsonify(args)
		else:
			response = jsonify({'Not the right ammount of args': 'needs to be between 1 and 3'})

		# response.status_code = 201
		return response

# exemplo: curl -H "Content-Type: application/json"  localhost:5000/connection -X post -d '{"SSID":"foo","Frequency":"1234","WEP":"1234123asdgwer"}'

class getlist(Resource):
	def get(self):
		response = jsonify('retornado valor do $iw list')
		return response

# exemplo: curl localhost:5000/getlist

class event(Resource):
	def get(self):
		response = jsonify('retornado valor do $iw event')
		return response
# exemplo: curl localhost:5000/event

class eventt(Resource):
	def get(self):
		response = jsonify('retornado valor do $iw event -t')
		return response
#exemplo: curl localhost:5000/eventt

class eventf(Resource):
	def get(self):
		response = jsonify('retornado valor do $iw event -f')
		return response
#exemplo: curl localhost:5000/eventf

class scan(Resource):
	def get(self):
		response = jsonify('retornado valor do $iw scan')
		return response
#exemplo: curl localhost:5000/scan

class stationstats(Resource):
	def get(self):
		response = jsonify('retornado valor do $iw dev wlan1 station dump')
		return response
#exemplo: curl localhost:5000/stationstats

class stationpeerstats(Resource):
	def get(self):
		response = jsonify('retornado valor do $ sudo iw dev wlan1 station get <peer-MAC-address>')
		return response
#exemplo: curl localhost:5000/stationpeerstats

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
api.add_resource(getlist, '/getlist')						#GET
api.add_resource(event, '/event')							#GET
api.add_resource(eventt,'/eventt')							#GET
api.add_resource(scan,'/scan')								#GET
api.add_resource(stationstats,'/stationstats')				#GET
api.add_resource(stationpeerstats, '/stationpeerstats')		#GET
api.add_resource(modlegacytxbitrates,'/modlegacytxbitrates')#POST
api.add_resource(modtxhtmcsbitrates,'/modtxhtmcsbitrates')	#POST
api.add_resource(settingtxpowerdev,'/settingtxpowerdev')	#POST
# api.add_resource(settingtxpowerphy,'/settingtxpowerphy')	#POST




if __name__ == '__main__':
	app.run(debug=True)