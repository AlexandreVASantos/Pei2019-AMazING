from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os
import subprocess
import sqlite3
import base64


user = {'username' : None, 'authenticated' : False }
url = 'http://10.110.1.149/rest/v3/'
grid = {}
cookie = {}

#function to receive wake up message from node, do not need csrf_cookie
@csrf_exempt
def node_up(request):
	if request.method == 'POST':
		try:
			args = json.loads(request.body.decode('utf-8'))
			print(args)
			node = args.get('node')
			print(node)
			connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/grid.db")
			c=connection.cursor()

			query = "Update node Set value='ON', color='green' where id="+ str(node) +";"
			#Only at this time we can update the value of the node in the database
			c.execute(query)
			connection.commit()
			connection.close()
			return render(request,'templates/Controller/node.html', {'message': 0})

		except sqlite3.Error as e:
			return render(request,'templates/Controller/node.html', {'message':'database error'})


	else:
		return render(request,'templates/Controller/node.html', {'message':'Wrong method'})


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
		return render(request,'templates/Controller/login.html', {'user': user, 'message' : 'Please fill both camps','failed': True})


	code=compLogin(username,password)
	

	if code[0] != 0:
		return render(request, 'templates/Controller/login.html',{'message' :'Authentication Failed','user' : user, 'failed': True })

	user["username"] = username
	user["authenticated"] = True
	
	return render(request,'templates/Controller/home.html',{ 'message': 'Authentication Sucessful', 'user' : user, 'success': True })

	

def log_out(request):
	user["username"] = None
	user["authenticated"] = False
	return render(request, 'templates/Controller/logout.html', {'message': 'Logout Sucessful', 'user' : user, 'success' : True})


def send_grid(request):
	refresh_grid()
	##use this block if a user login is added to the switch
	#sess = requests.Session()
	#req = sess.post(url + 'login-sessions',,timeout=1)
	#cookie_response = req.json()['cookie']
	#cookie = {'cookie : cookie_response'}
	node_grid = grid
	
	return render(request,'templates/Controller/config.html',{'node_grid':node_grid, 'user' : user})
	
	

def refresh_grid():
	try:	
		connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/grid.db")
		c=connection.cursor()	
		c.execute("Select * from node;")
		fetch= c.fetchall()
		for row in fetch:
			grid[row[0]] = (row[1],row[2],row[3])
		connection.close()
		return 0,grid
	except sqlite3.Error as e:
		return 1,str(e)

def grid_update(request):
	node_grid = refresh_grid()
	return render(request,'templates/Controller/config.html',{'node_grid':node_grid, 'message': message, 'user' : user, 'success': True })
	
def send_commands(command):
	command_bytes = command.encode()
	command_base64 = base64.b64encode(command_bytes)
	command_dict={'cli_batch_base64_encoded': command_base64.decode('utf-8')}
	post_command = requests.post(url + 'cli_batch', headers=cookie, data=json.dumps(command_dict), timeout=1)
	return post_command

def change_grid(request):
	
	#url = "http://httpbin.org/post"
	
	#data = {"data":"123"}
	dic=request.POST
	for key in dic:
		node=key
		value=dic[key]

	(val,color,portId) = grid[int(node)]

	if value == 'OFF':
			#if value OFF turn on
			commands = "interface" + str(portId) + "\npower-over-ethernet\n"

			#can't update database immediately, need to wait for node to go up
			code = send_commands(commands)

			if code != 202:
				return render(request, 'Controller/error.html', {'error': 'commands not accepted'})
	else:
		try:
			connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/grid.db")
			c=connection.cursor()
			
		
			#if value ON turn off
			commands = "interface" + str(portId) + "\nno power-over-ethernet\n"

			query = "Update node Set value='OFF', color='red' where id=" + str(node) +";"
			print("asdnasdhaksdhas")
		
			code = send_commands(commands)
			if code != 202:
				return render(request, 'Controller/error.html', {'error': 'commands not accepted'})

			#update value of node state in database
			c.execute(query)
			connection.commit()
			connection.close()


			E_id,error = refresh_grid()
			if E_id == 1:
				return render(request, 'templates/Controller/error.html', {'error': error,'user' : user})

		except sqlite3.Error as e:
			return render(request, 'templates/Controller/error.html', {'error': str(e),'user' : user})
		
	

	node_grid = grid
	#data_json= json.dumps(data)
	#headers = {'Content-Type': 'application/json'}
	#req= requests.post(url,data=data_json, headers=headers)
	#print(req.json())
	
	return render(request,'templates/Controller/config.html',{'node_grid':node_grid, 'user': user})


def error_404(request):
	return render(request, 'templates/Controller/notfound.html', {"error":"404 Page not found",'user' : user})

def error_500(request):
	return render(request, 'templates/Controller/notfound.html', {"error": "Error 500",'user' : user})