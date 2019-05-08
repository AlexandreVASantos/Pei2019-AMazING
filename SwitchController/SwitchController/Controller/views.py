from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import json
import requests
import os
import subprocess
import sqlite3
import base64
import time


user = {'username' : None, 'authenticated' : False }
url = 'http://10.110.1.149/rest/v3/'
grid = {}
cookie = {}
alert = False

#function to receive data from node sensors, do not need csrf_cookie
@csrf_exempt
def sensors(request):
	if request.method == 'POST':
		try:
			args = json.loads(request.body.decode('utf-8'))
			
			node = args.get('node')
			info = args.get('readings')
			date = args.get('date')
			
			connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/controller.db")
			c=connection.cursor()

			query = "Insert into alerts values(" + str(node)+ ",'" + str(info)+ "','"+ str(date) +"','False');"
			#Only at this time we can update the value of the node in the database
			c.execute(query)
			connection.commit()
			connection.close()
			global alert
			alert = True

			return render(request,'templates/Controller/node.html', {'message': 0})

		except sqlite3.Error as e:
			return render(request,'templates/Controller/node.html', {'message':'database error'})


	else:
		return render(request,'templates/Controller/node.html', {'message':'Wrong method'})







#function to receive wake up message from node, do not need csrf_cookie
@csrf_exempt
def node_up(request):
	if request.method == 'POST':
		try:
			args = json.loads(request.body.decode('utf-8'))
			print(args)
			node = args.get('node')
			print(node)
			connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/controller.db")
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



def manual(request):
	return render(request,'templates/Controller/manual.html', {'user': user, 'alert' : alert})



def home(request):
	return render(request,'templates/Controller/home.html', {'user': user, 'alert' : alert})



def getlogin(request):
	return render(request,'templates/Controller/login.html', {'user': user})





def compLogin(username, password):
	try:
		connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/controller.db")
		c=connection.cursor()
		query="Select username, password from users where username= '" + str(username) + "';"
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


	
	return render(request,'templates/Controller/home.html',{ 'message': 'Authentication Sucessful', 'user' : user, 'success': True,  'alert': alert})



def change_pass(request):
	username = request.POST.get('username')
	o_pass = request.POST.get('old_password')
	n_pass = request.POST.get('new_password')
	r_pass = request.POST.get('rewrite_password')
	print(request.POST)

	if username != 'AmazingManager':
		return render(request, 'templates/Controller/password.html',{'message' :'Wrong username' ,'user' : user, 'failed': True  })


	if n_pass != r_pass or n_pass is None or n_pass == '':
		return render(request, 'templates/Controller/password.html',{'message' :'New passwords did not match' ,'user' : user, 'failed': True  })

	try:
		connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/controller.db")
		c=connection.cursor()
		query1="Select username, password from users where username='" + str(username) + "';"
		print(username)
		c.execute(query1)
		fetch= c.fetchall()
		print(fetch)
		if fetch[0][1] != o_pass:
			connection.close()
			return render(request, 'templates/Controller/password.html',{'message' :'Old password did not match' ,'user' : user, 'failed': True  })

		query2 = "Update users set password='" +  str(n_pass) + "'where username= '" + str(username) + "';"
		c.execute(query2)
		connection.commit()
		connection.close()
		return render(request, 'templates/Controller/login.html',{'message' :'Password changed with success' ,'user' : user, 'success': True  })
	except sqlite3.Error as e:
		return render(request, 'templates/Controller/error.html',{'error' :"Can't access database at the moment ",'user' : user  })




def password(request):
	return render(request, 'templates/Controller/password.html')




def log_out(request):
	user["username"] = None
	user["authenticated"] = False
	return render(request, 'templates/Controller/logout.html', {'message': 'Logout Sucessful', 'user' : user, 'success' : True})





	
def get_notifications_with_date(request):
	print(request.POST)
	
	try:

		values = request.POST

		date_init = values.get('date1')
		date_final = values.get('date2')
		node = values.get('node_id')

		if node is None or node == '':
			if date_init is None or date_init == '' or date_final is None or date_final == '':
				return render(request, 'templates/Controller/notifications.html',{'failed': True, 'message' :' Please fill at least node field or both data fields' ,'user': user})

			else:
				date1 = time.strptime(date_init, "%Y-%m-%d")
				date2 = time.strptime(date_final, "%Y-%m-%d")
				if date2 < date1:
					return render(request, 'templates/Controller/notifications.html',{'failed': True, 'message' :' Final date must be bigger than initial date.' ,'user': user})

				date_in =str(date_init) + ' 00:00:00.000'
				print(date_init)
				date_fin = str(date_final) + ' 23:59:59.999'
				query="Select node_id, alert, date_alert from alerts where date_alert >='" +str(date_in)+ "' AND date_alert <='" +str(date_fin)+ "';"

		else:
			if date_init is None or date_init == '' or date_final is None or date_final == '':
				query="Select node_id, alert, date_alert from alerts where node_id= " + str(node) + " Order by date_alert Desc;"
			else:
				date1 = time.strptime(date_init, "%Y-%m-%d")
				date2 = time.strptime(date_final, "%Y-%m-%d")
				if date2 < date1:
					return render(request, 'templates/Controller/notifications.html',{'failed': True, 'message' :' Final date must be bigger than initial date.' ,'user': user})

				date_in =str(date_init) + ' 00:00:00.000'
				print(date_init)
				date_fin = str(date_final) + ' 23:59:59.999'
				query = query="Select node_id, alert, date_alert from alerts where date_alert >='" +str(date_in)+ "' AND date_alert <='" +str(date_fin)+ "' AND node_id=" + str(node) + ";"
		
		connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/controller.db")
		c=connection.cursor()
			
		c.execute(query)
		fetch= c.fetchall()
		connection.close()
		value = [('node '+str(x[0]), x[1].split('\n'), x[2]) for x in fetch]
	except sqlite3.Error as e:
		return render(request, 'templates/Controller/error.html',{'error': str(e),'user': user})

	return render(request, 'templates/Controller/notifications.html',{'user': user, 'alert' : alert, 'notifications':value, 'date1' : str(date_init), 'date2': str(date_final), 'node' : str(node)})



def get_notifications():
	try:
		connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/controller.db")
		c=connection.cursor()
		query="Select node_id, alert, date_alert from alerts where read = 'False' Order by date_alert Desc;" 
		c.execute(query)
		fetch= c.fetchall()
		for x in fetch:
			query_up = "Update alerts set read = 'True' where node_id = " +str(x[0])+ " AND date_alert= '" +str(x[2])+ "';"
			c.execute(query_up)
			connection.commit()
		connection.close()
		notifications = [('node '+ str(x[0]), x[1].split('\n'),x[2]) for x in fetch]
		print(notifications)
		return 0,notifications
	except sqlite3.Error as e:
		return 1,str(e)	



def notifications(request):
	global alert
	alert = False
	error,value = get_notifications();
	if error == 1:
		return render(request, 'templates/Controller/error.html',{'error': str(value),'user': user})

	return render(request, 'templates/Controller/notifications.html',{'user': user, 'alert' : alert, 'notifications':value })




def send_grid(request):
	refresh_grid()
	##use this block if a user login is added to the switch
	#sess = requests.Session()
	#req = sess.post(url + 'login-sessions',,timeout=1)
	#cookie_response = req.json()['cookie']
	#cookie = {'cookie : cookie_response'}
	node_grid = grid
	
	return render(request,'templates/Controller/config.html',{'node_grid':node_grid, 'user' : user, 'alert': alert})
	
	

def refresh_grid():
	try:	
		connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/controller.db")
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
	code,node_grid = refresh_grid()
	if code == 1:
		return render(request, 'templates/Controller/error.html',{'error': "Can't refresh grid at the moment. Try again later.",'user': user, 'alert':alert})

	return render(request,'templates/Controller/config.html',{'node_grid': node_grid, 'user' : user,  'alert': alert})





	
def send_commands(command):
	command_bytes = command.encode()
	command_base64 = base64.b64encode(command_bytes)
	command_dict={'cli_batch_base64_encoded': command_base64.decode('utf-8')}
	post_command = requests.post(url + 'cli_batch', data=json.dumps(command_dict), timeout=1)
	return post_command




	

def change_grid(request):
	
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
			connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/controller.db")
			c=connection.cursor()
			
			#if value ON turn off
			commands = "interface" + str(portId) + "\nno power-over-ethernet\n"

			query = "Update node Set value='OFF', color='red' where id=" + str(node) +";"
		
		
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
	
	
	return render(request,'templates/Controller/config.html',{'node_grid':node_grid, 'user': user, 'alert': alert})


def error_404(request):
	return render(request, 'templates/Controller/notfound.html', {"error":"404 Page not found",'user' : user,'alert': alert})

def error_500(request):
	return render(request, 'templates/Controller/notfound.html', {"error": "Error 500",'user' : user,'alert': alert})