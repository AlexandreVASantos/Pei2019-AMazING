from flask import Flask,jsonify, request, json
from flask_restful import Api, Resource


app = Flask(__name__)



@app.route('/')
def hello_world():
    return 'Hello World'

class Login(Resource):
	def post(self):
		credentials={'userName' : '{}'.format(), 'password' : '{}'.format()}
		return
	
class Logout(Resource):
	def post(self):
		command = {'cmd' : 'logout'}
		return
	

class Poe_disable(Resource):
	def post(self):
		command = {'cmd': ['configure terminal','interface {}'.format(),'power-over-ethernet']}
		return
	

class Poe_enable(Resource):
	def post(self):
		command = {'cmd': ['configure terminal','interface {}'.format(),'no power-over-ethernet']}
		return
	

api.add_resource(Login,'/rest/v1/login-sessions')
api.add_resource(Logout,'/rest/v3/cli')
api.add_resource(Poe_disable,'/rest/v3/cli')
api.add_resource(Poe_enable,'/rest/v3/cli')


if __name__ == '__main__':
	app.run(debug=True)