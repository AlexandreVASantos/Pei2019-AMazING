from django.shortcuts import render, redirect

import json
import requests
import os
import subprocess
import sqlite3
import base64


user = {'username' : None, 'authenticated' : False }
#url = 'http://x.x.x.x/rest/v3/'
grid = {}
cookie = {}

# Create your views here.
def home(request):
	return render(request,'templates/Controller/home.html', {'user': user})

def getlogin(request, message = None):
	return render(request,'templates/Controller/login.html', {'user': user})


def compLogin(username, password):
	try:
		connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/grid.db")
		c=connection.cursor()
		query='Select username, password from users where username= "' + username + '";'
		c.execute(query)
		fetch= c.fetchall()
		print(fetch)
		if fetch[0][1] != password:
			connection.close()
			return 1, 'Wrong password'
		connection.close()
		return 0,None
	except sqlite3.Error as e:
		return 1,str(e)

def log_in(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	if username == '' or password == '':
		#return redirect('http://127.0.0.1:8000/getlogin/')
		return render(request,'templates/Controller/login.html', {'user': user, 'message' : 'Please fill both camps','failed': True})

	print(username,password)

	code=compLogin(username,password)
	

	if code[0] != 0:
		return render(request, 'templates/Controller/login.html',{'message' :'Authentication Failed','user' : user, 'failed': True })

	user["username"] = username
	user["authenticated"] = True
	return send_grid(request, 'Authentication Sucessful')

def log_out(request):
	user["username"] = None
	user["authenticated"] = False
	return render(request, 'templates/Controller/logout.html', {'message': 'Logout Sucessful', 'user' : user, 'success' : True})


def send_grid(request, message = None):
	refresh_grid()
	#sess = requests.Session()
	#req = sess.post(url + 'login-sessions',,timeout=1)
	#cookie_response = req.json()['cookie']
	#cookie = {'cookie : cookie_response'}
	node_grid = grid
	if message == None:
		return render(request,'templates/Controller/config.html',{'node_grid':node_grid, 'user' : user})
	else:
		return render(request,'templates/Controller/config.html',{'node_grid':node_grid, 'message': message, 'user' : user, 'success': True })


def refresh_grid():
	try:	
		connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/grid.db")
		c=connection.cursor()	
		c.execute("Select * from node;")
		fetch= c.fetchall()
		for row in fetch:
			grid[row[0]] = (row[1],row[2],row[3])
		connection.close()
		return 0,[]
	except sqlite3.Error as e:
		return 1,str(e)
	
#def send_commands(command):
	#command_bytes = command.encode()
	#command_base64 = base64.b64encode(command_bytes)
	#command_dict={'cli_batch_base64_encoded': command_base64.decode('utf-8')}
	#post_command = requests.post(url + 'cli_batch', headers=, data=json.dumps(command_dict), timeout=1)
	#return post_command

def send_shit(request):
	#os.system('ping google.com')
	temp_grid = grid
	subprocess.check_call(['echo','SWITCH ARUBA'])
	#url = 'http://192.1.1.1/connection'
	url = "http://httpbin.org/post"
	#data = {"SSID":"foo","Frequency":"1234","WEP":"1234123asdgwer"}
	data = {"data":"123"}
	dic=request.GET
	for key in dic:
		node=key
		value=dic[key]

	(val,color,portId) = grid[int(node)]

	try:
		connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/grid.db")
		c=connection.cursor()
		
		try:
			if value == 'OFF':
				#turn on
				#comands = 'telnet x.x.x.x configure terminal interface' + grid[int(node)][2] + 'power-over-ethernet end write memory'
				#command = 'telnet x.x.x.x show running-config'
				#commands = "interface" + portId + "\npower-over-ethernet\n"
				#code = send_command(commands)
				#subprocess.check_output(comands)
				#if code != 202:
					#render(request, 'Controller/error.html', {'error': 'commands not accepted'})
				query = "Update node Set value='ON', color='green' where id="+ node +";"
			else:
				#turn off
				#comands = 'telnet x.x.x.x configure terminal interface' + grid[int(node)][2] + ' no power-over-ethernet end write memory'
				#command = 'telnet x.x.x.x show running-config'
				#commands = "interface" + portId + "\nno power-over-ethernet\n"
				
				#subprocess.check_output(comands)
				#if code != 202:
					#render(request, 'Controller/error.html', {'error': 'commands not accepted'})
				
				query = "Update node Set value='OFF', color='red' where id=" + node +";"
		except subprocess.CalledProcessError as e:
			return render(request, 'templates/Controller/error.html', {'error': e.stderr, 'user' : user})


		c.execute(query)
		connection.commit()
		connection.close()
	except sqlite3.Error as e:
		return render(request, 'templates/Controller/error.html', {'error': str(e),'user' : user})
	#
	
	E_id,error = refresh_grid()
	if E_id == 1:
		return render(request, 'templates/Controller/error.html', {'error': error,'user' : user})

	node_grid = grid
	data_json= json.dumps(data)
	headers = {'Content-Type': 'application/json'}
	req= requests.post(url,data=data_json, headers=headers)
	print(req.json())
	
	return render(request,'templates/Controller/config.html',{'node_grid':node_grid, 'user': user})


def error_404(request):
	return render(request, 'templates/Controller/notfound.html', {"error":"404 Page not found",'user' : user})

def error_500(request):
	return render(request, 'templates/Controller/notfound.html', {"error": "Error 500",'user' : user})