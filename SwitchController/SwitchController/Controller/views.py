from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from dateutil import relativedelta
from django.http import JsonResponse
from background_task import background
from kafka import KafkaConsumer
from kafka import TopicPartition
from kafka.structs import OffsetAndMetadata
from kafka.errors import NoBrokersAvailable
import json
import requests
import os
import subprocess
import sqlite3
import base64
import time
import datetime


user = {'username' : None, 'authenticated' : False }
url = 'http://switchIP/rest/v3/'

headers = {'cookie': ''}

grid = {}
cookie = {}
alert = False
node_up=0
power_supply=0
request_node = False

count_alive={"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0,"24":0 }
count_time=0



@background(schedule=1)
def check_reading_messages():
	while(True):
		count = 0
		try:
			global count_time
			global alert
			
			time.sleep(10)
			consumerA = KafkaConsumer('alerts', bootstrap_servers=['192.168.85.228:9093'], auto_offset_reset='earliest',enable_auto_commit=False, group_id="get_alerts", value_deserializer=lambda x:json.loads(x.decode('utf-8')), consumer_timeout_ms=3000)
			connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
			c = connection.cursor()
			
			for message in consumerA:
				meta = consumerS.partitions_for_topic(message.topic)
				partition = TopicPartition(message.topic, message.partition)
				offsets = OffsetAndMetadata(message.offset +1 , meta)
				options = {partition: offsets}
				consumerS.commit(offsets=options)
				
				

				message= message.value
		
				for (n_id, info) in message.items():
					query = "Insert into alerts values(" + str(node_id)+ ",'" + str(info[1])+ "','"+ str(info[0]) +"','False');"
					count +=1
					c.execute(query)
					connection.commit()

			if count != 0:
				alert = True
		
			consumerA.close()
		
			time.sleep(50)
		
			
			consumerS = KafkaConsumer('switch', bootstrap_servers=['192.168.85.228:9093'], auto_offset_reset='earliest',enable_auto_commit=False, group_id="get_alive", value_deserializer=lambda x:json.loads(x.decode('utf-8')), consumer_timeout_ms=3000)
			for message in consumerS:
				
				meta = consumerS.partitions_for_topic(message.topic)
				partition = TopicPartition(message.topic, message.partition)
				offsets = OffsetAndMetadata(message.offset +1 , meta)
				options = {partition: offsets}
				consumerS.commit(offsets=options)

				message = message.value
				
			
				for (n_id, reading) in message.items():
					if str(reading) == 'wake_up':
						todays_date = datetime.datetime.now()
						date = todays_date.strftime("%Y-%m-%d %H:%M:%S")
						query = "Update node Set value='ON', dateOn = '" + str(date) +"' where id=" + str(n_id) +";"
						c.execute(query)
						connection.commit()
					else:
						query = "Select value from node where id=" + str(n_id)+";"
						c.execute(query)
						fetch = c.fetchone()[0]
						if fetch == "OFF" and count_alive[str(n_id)] > 1:
							todays_date = datetime.datetime.now()
							date = todays_date.strftime("%Y-%m-%d %H:%M:%S")
							"Update node Set value='ON', dateOn = '" + str(date) +"' where id=" + str(n_id) +";"
							c.execute(query)
							connection.commit()
						count_alive[str(n_id)] +=1
			
			consumerS.close()
			

			if count_time == 5:
				for i in range(1,25):
					if count_alive[str(i)] == 0:
							query = "Update node Set value='OFF', dateOn = '0' where id=" + str(i) +";"
							c.execute(query)
							connection.commit()
					else:
						count_alive[str(i)] = 0
				count_time = 0

			

			count_time+=1

			c.close()	
			connection.close()
		
		except sqlite3.Error as e:
			continue
		except NoBrokersAvailable as e:
			pass


		
		




# #function to receive data from node sensors, do not need csrf_cookie
# @csrf_exempt
# def sensors(request):
# 	if request.method == 'POST':
# 		#try:
# 		args = json.loads(request.body.decode('utf-8'))
		
# 		node = args.get('alive')
# 			# node = args.get('node')
# 			# info = args.get('readings')

# 			# todays_date = datetime.datetime.now()
# 			# date = todays_date.strftime("%Y-%m-%d %H:%M:%S")
# 		count_alerts['node'] +=1
			
# 			# connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
# 			# c=connection.cursor()

# 			# query = "Insert into alerts values(" + str(node)+ ",'" + str(info)+ "','"+ str(date) +"','False');"
# 			# #Only at this time we can update the value of the node in the database
# 			# c.execute(query)
# 			# connection.commit()
# 			# connection.close()
# 			# global alert
# 			# alert = True

# 			#return render(request, 'templates/Controller/home.html', {'message' : 0})

# 		#except sqlite3.Error as e:			
# 		#	return render(request, 'templates/Controller/home.html', {'message' : 'database error'})
# 		return JsonResponse({'code':0})

# 	else:
# 		return render(request, 'templates/Controller/home.html')








#function to receive wake up message from node, do not need csrf_cookie
# @csrf_exempt
# def node_up(request):
# 	if request.method == 'POST':
# 		try:
# 			args = json.loads(request.body.decode('utf-8'))
# 			node = args.get('node')
# 			up_date = datetime.datetime.now()
# 			time2 = up_date
# 			date = up_date.strftime("%Y-%m-%d %H:%M:%S")
# 			connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
# 			c=connection.cursor()

# 			query = "Update node Set value='ON', dateOn='"+ str(date) + "' where id="+ str(node) +";"
# 			#Only at this time we can update the value of the node in the database
# 			c.execute(query)
# 			connection.commit()
# 			c.close()
# 			connection.close()
# 			return render(request, 'templates/Controller/home.html', {'message' : 0})

# 		except sqlite3.Error as e:			
# 			return render(request, 'templates/Controller/home.html', {'message' : 'database error'})


# 	else:
# 		return render(request, 'templates/Controller/home.html')



def manual(request):
	return render(request,'templates/Controller/manual.html', {'user': user, 'alert' : alert, 'request':request_node})



def home(request):
	##if will check if there's any alert to show to the user
	if request.is_ajax():
		global alert
		if alert == False:
			alert = alerts()
		return JsonResponse({'alert':alert, 'user':user})

	return render(request,'templates/Controller/home.html', {'user': user, 'alert' : alert, 'request':request_node})


def getlogin(request):
	return render(request,'templates/Controller/login.html', {'user': user})



@csrf_exempt
def request(request):
	if request.method == 'POST':
		global request_node
		try:
			args = json.loads(request.body.decode('utf-8'))

			node = args.get('id')
			username = args.get('username')
			connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
			c=connection.cursor()

			query = "Select id,value from node where id="+ str(node) +";"
			c.execute(query)
			fetch = c.fetchone()
			c.close()
			connection.close()
		except sqlite3.Error as e:
			return JsonResponse({'code':2})

		if fetch[1] == 'ON':
			return JsonResponse({'code':0})
		else:

			request_node = True

			try:
				connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
				c=connection.cursor()
				query= "Select username from requests where username='" +str(username)+ "' and node_id=" + str(node) + " and requested != 'False';"
				c.execute(query)
				fetch1 = c.fetchone()
				query= "Select username from requests where username='" +str(username)+ "' and node_id=" + str(node) + " and requested == 'False';"
				c.execute(query)
				fetch2 = c.fetchone()
				if fetch1 is None:
					if fetch2 is None:
						query = "Insert into requests values (" +str(node) + ",'"+ str(username)+"' ,'True')"
						c.execute(query)
						connection.commit()
					else:
						query = "Update requests set requested= 'True' where node_id = "+ str(node)+" and username='" + str(username)+ "';"
						c.execute(query)
						connection.commit()
				
				c.close()
				connection.close()
				return JsonResponse({'code':1})
			except sqlite3.Error as e:
				return JsonResponse({'code':2})
			
			return JsonResponse({'code':1})

	else:
		return render(request, 'templates/Controller/home.html',{'user': user, 'alert': alert, 'request':request_node})




@csrf_exempt
def reset_node(request):
	if request.method == 'POST':
		if request.is_ajax():
			try:
				connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
				c=connection.cursor()
				
				node = request.POST.get('id')
				
				code = refresh_grid()

				if code[0] == 1:
					return JsonResponse({'code': -1})

				(val,color,portId) = grid[int(node)]

				
				commands = "conf t\ninterface " + str(portId) + "\nno power-over-ethernet\nwrite memory"

				
				code,post = send_commands(commands)

				if code != 0:
					return JsonResponse({'code': -1})


				

				if post.status_code != 202:
					return JsonResponse({'code': -1})

				query = query = "Update node Set value='OFF', dateOn = '0' where id=" + str(node) +";"

				c.execute(query)
				connection.commit()

				c.close
				connection.close()


				commands = "conf t\ninterface " + str(portId) + "\npower-over-ethernet\nwrite memory"

				time.sleep(3)
				
				code,post = send_commands(commands)
				if code !=0:
					return JsonResponse({'code': -1})

				

				if post.status_code != 202 :
					return JsonResponse({'code': -1})

				

				return JsonResponse({'code' : 200})

			except sqlite3.Error as e:
				return JsonResponse({'code' : -1})

			
		return JsonResponse({'code' : -1})

	return render(request, 'templates/Controller/home.html', {'user':user})


@csrf_exempt
def requests_on(request):
	if request.method== 'GET':
		global request_node
		#if request is ajax and request_node is True then a notification is shown to the user
		if request.is_ajax():
			return JsonResponse({'user':user, 'request':request_node})
		try:
			connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
			c=connection.cursor()
			query = "Delete from requests where requested = 'False';"
			c.execute(query)
			connection.commit()
			query = "Select username, node_id from requests where requested='True';"
			c.execute(query)
			fetch = c.fetchall()
			c.close()
			connection.close()
			for row in fetch:
				if row[0] in requests:
					requests[row[0]].append(row[1])
				else:
					requests[row[0]] = row[1] 

		except sqlite3.Error as e:
			return render(request, 'templates/Controller/error.html',{'error' :"Can't access database at the moment ",'user' : user  })

		request_node = False

		
		return render(request, 'templates/Controller/requests.html',{'user': user, 'alert': alert, 'request':request_node,'requests': requests})
	else:
		if request.method == 'POST':
			if request.is_ajax():
				node_id = request.POST.get('id')
				username = request.POST.get('username')

				try:
					connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
					c=connection.cursor()
					query = "Update requests set requested = 'False' where node_id=" + str(node_id) + " AND username='" + str(username) + "';"
					c.execute(query)
					connection.commit()
					c.close()
					connection.close()

					return JsonResponse({"code" : 200})

				except sqlite3.Error as e:
					return render(request, 'templates/Controller/error.html',{'error' :"Can't access database at the moment ",'user' : user  })
			
			return render(request, 'templates/Controller/home.html',{'user' : user  })
		
		return render(request, 'templates/Controller/home.html',{'user' : user  })
		




##Check if there is any alert not read yet
def alerts():
	try:
		connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
		c=connection.cursor()
		query="Select count(*) from alerts where read = 'False';" 
		c.execute(query)
		fetch= c.fetchone()[0]
		
		c.close()
		connection.close()
		if fetch != 0:
			return True
		return False
	except sqlite3.Error as e:
		return False

	

def compLogin(username, password):
	try:
		connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
		c=connection.cursor()
		query="Select username, password from users where username= '" + str(username) + "';"
		c.execute(query)
		fetch= c.fetchall()
		
		if fetch[0][1] != password:
			c.close()
			connection.close()
			return 1, 'Wrong password'
		c.close()
		connection.close()
		return 0,None
	except sqlite3.Error as e:
		return 1,str(e)



def log_in(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		if username == '' or password == '':
			return render(request,'templates/Controller/login.html', {'user': user, 'message' : 'Please fill both camps','failed': True})


		code=compLogin(username,password)
		

		if code[0] != 0:
			return render(request, 'templates/Controller/login.html',{'message' :'Authentication Failed','user' : user, 'failed': True })

		##use this block if a user login is added to the switch, and the cookie needs to be passed to every post to the switch as a header field
		#sess = requests.Session()
		#req = sess.post(url + 'login-sessions',data={},timeout=1)
		#cookie_response = req.json()['cookie']
		#cookie = {'cookie : cookie_response'}
		#if req.status_code != 201:
		#	return render(request, 'Controller/error.html', {'error': 'could not connect to the Switch'})


		user["username"] = username
		user["authenticated"] = True

		global alert

		if alert == False:
			alert = alerts()


		
		return render(request,'templates/Controller/home.html',{ 'message': 'Authentication Sucessful', 'user' : user, 'success': True,  'alert': alert})
	else:
		return render(request, 'templates/Controller/login.html',{'user' : user})

def change_pass(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		o_pass = request.POST.get('old_password')
		n_pass = request.POST.get('new_password')
		r_pass = request.POST.get('rewrite_password')

		##Checks username
		if username != 'AmazingManager':
			return render(request, 'templates/Controller/password.html',{'message' :'Wrong username' ,'user' : user, 'failed': True  })

		##Checks if new passwords are empty
		if n_pass != r_pass or n_pass is None or n_pass == '':
			return render(request, 'templates/Controller/password.html',{'message' :'New passwords did not match' ,'user' : user, 'failed': True  })

		try:
			connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
			c=connection.cursor()
			query1="Select username, password from users where username='" + str(username) + "';"
			c.execute(query1)
			fetch= c.fetchone()

			##Check if the old password match
			if fetch[1] != o_pass:
				connection.close()
				return render(request, 'templates/Controller/password.html',{'message' :'Old password did not match' ,'user' : user, 'failed': True  })

			query2 = "Update users set password='" +  str(n_pass) + "'where username= '" + str(username) + "';"
			c.execute(query2)
			connection.commit()
			c.close()
			connection.close()
			return render(request, 'templates/Controller/login.html',{'message' :'Password changed with success' ,'user' : user, 'success': True  })
		except sqlite3.Error as e:
			return render(request, 'templates/Controller/error.html',{'error' :"Can't access database at the moment ",'user' : user  })
	else:
		return render(request, 'templates/Controller/password.html',{'user' : user})



def password(request):
	return render(request, 'templates/Controller/password.html')




def log_out(request):
	user["username"] = None
	user["authenticated"] = False
	return render(request, 'templates/Controller/logout.html', {'message': 'Logout Sucessful', 'user' : user, 'success' : True})



	
def get_notifications_with_date(request):

	if request.method == 'POST':
	
		try:

			values = request.POST

			date_init = values.get('date1')
			date_final = values.get('date2')
			node = values.get('node_id')

			if node is None or node == '':
				if date_init is None or date_init == '' or date_final is None or date_final == '':
					return render(request, 'templates/Controller/notifications.html',{'failed': True, 'message' :' Please fill at least node field or both data fields' ,'user': user})

				else:
					date1 = datetime.datetime.strptime(date_init, "%Y-%m-%d")
					date2 = datetime.datetime.strptime(date_final, "%Y-%m-%d")
					if date2 < date1:
						return render(request, 'templates/Controller/notifications.html',{'failed': True, 'message' :' Final date must be bigger than initial date.' ,'user': user})

					date_in =str(date_init) + ' 00:00:00'
					
					date_fin = str(date_final) + ' 23:59:59'
					query="Select node_id, alert, date_alert from alerts where date_alert >='" +str(date_in)+ "' AND date_alert <='" +str(date_fin)+ "';"

			else:
				if date_init is None or date_init == '' or date_final is None or date_final == '':
					if isinstance(int(node), int):
						if int(node) < 1 or int(node) > 24:
							return render(request, 'templates/Controller/notifications.html',{'failed': True, 'message' :' Node number must be between 1 and 24.' ,'user': user})
					query="Select node_id, alert, date_alert from alerts where node_id= " + str(node) + " Order by date_alert Desc;"
				else:
					date1 = datetime.datetime.strptime(date_init, "%Y-%m-%d")
					date2 = datetime.datetime.strptime(date_final, "%Y-%m-%d")
					if date2 < date1:
						return render(request, 'templates/Controller/notifications.html',{'failed': True, 'message' :' Final date must be bigger than initial date.' ,'user': user})

					date_in =str(date_init) + ' 00:00:00'
					
					date_fin = str(date_final) + ' 23:59:59'
					query = query="Select node_id, alert, date_alert from alerts where date_alert >='" +str(date_in)+ "' AND date_alert <='" +str(date_fin)+ "' AND node_id=" + str(node) + ";"
			
			connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
			c=connection.cursor()
				
			c.execute(query)
			fetch= c.fetchall()
			c.close()
			connection.close()
			value = [('node '+str(x[0]), x[1].split('\n'), x[2]) for x in fetch]
		except sqlite3.Error as e:
			return render(request, 'templates/Controller/error.html',{'error': "Can't access database at the moment.",'user': user})
		except ValueError:
			return render(request, 'templates/Controller/notifications.html',{'failed': True, 'message' :' Node must be a number between 1 and 24' ,'user': user})

		return render(request, 'templates/Controller/notifications.html',{'user': user, 'alert' : alert,  'request':request_node,'notifications':value, 'date1' : str(date_init), 'date2': str(date_final), 'node' : str(node)})
	else:
		return render(request, 'templates/Controller/notifications.html',{'user': user})
	



def notifications(request):
	try:
		global alert
		alert = False
		connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
		c=connection.cursor()
		query="Select node_id, alert, date_alert from alerts where read = 'False' Order by date_alert Desc;" 
		c.execute(query)
		fetch= c.fetchall()
		for row in fetch:
			query_up = "Update alerts set read = 'True' where node_id = " +str(row[0])+ " AND date_alert= '" +str(row[2])+ "';"
			c.execute(query_up)
			connection.commit()
		connection.close()
		notifications = [('node '+ str(row[0]), row[1].split('\n'),row[2]) for row in fetch]

	except sqlite3.Error as e:
		return render(request, 'templates/Controller/error.html',{'error': "Can't access database at the moment",'user': user})

	return render(request, 'templates/Controller/notifications.html',{'user': user, 'alert' : alert, 'request':request_node, 'notifications': notifications})


def stats(request):

	try:
		connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
		c=connection.cursor()

		##count how many alerts exist
		query1="Select count(*) from alerts;" 	
		c.execute(query1)
		numAlerts = c.fetchone()[0]
		

		##count how many nodes are ON
		query2="Select count(id) from node where value='ON';" 	
		c.execute(query2)
		numOn = c.fetchone()[0]
		
		
		## fill dict to alerts graphic
		query3 = "Select node_id, count(alert) from alerts group by node_id;"
		c.execute(query3)
		fetch_alerts = c.fetchall()

		
		numAlertsNode={}
		for info in fetch_alerts:
			numAlertsNode[info[0]] = int(info[1])

		for i in range(1,25):
			if i not in list(numAlertsNode.keys()):
				numAlertsNode[i] = 0


		
		## fill dict to hours graphic
		todays_date = datetime.datetime.now()
		query4 = "Select id, dateOn from node where dateOn != '0';"
		c.execute(query4)
		fetch_hours = c.fetchall()
		

		numHours={}
		for info in fetch_hours:
			#date when node was turned on
			up_date = datetime.datetime.strptime(info[1],'%Y-%m-%d %H:%M:%S') 
			#difference between actual date and up_date
			difference = relativedelta.relativedelta(todays_date,up_date)
			if int(difference.months) != 0:
				numHours[info[0]]= int(difference.months)*30*24 + int(difference.days)*24 + int(difference.hours)
			elif int(difference.days) != 0 :
				numHours[info[0]] = int(difference.days)*24 + int(difference.hours)
			else:
				numHours[info[0]] = int(difference.hours)

		for i in range(1,25):
			if i not in list(numHours.keys()):
				numHours[i] = 0

		
		c.close()
		connection.close()
	
	except sqlite3.Error as e:
		if request.is_ajax():
			return JsonResponse({'code': -1})
		return render(request, 'templates/Controller/error.html',{'error': "Can't access database at the moment",'user': user})

		
	

	if request.is_ajax():
		return JsonResponse({'node_up':str(numOn), 'hours' : numHours,'n_alerts_node': numAlertsNode ,'n_alerts': str(numAlerts)})

	
	return render(request, 'templates/Controller/stats.html', {'user' : user,'alert' : alert, 'request':request_node, 'node_up':str(numOn), 'hours' : numHours,'n_alerts_node': numAlertsNode ,'n_alerts': str(numAlerts)})

def stats_poe(request):
	#command to show poe info
	if request.is_ajax():

		code,info = send_commands_power()
		if code == 1:
			return JsonResponse({'code': -1,'error': 'Cannot access swith at the moment'})
		
		
		if info.status_code != 200 :
			return JsonResponse({'code': -1, 'error': 'commands not accepted'})
		else:
			response = info.json()['result_base64_encoded']
			decoded_r = base64.b64decode(response).decode('utf-8')
			
			
			return JsonResponse({'code': 200, 'info': decoded_r.split('\n')})
	else:
		return stats(request)
		
def send_commands_power():
	##sequence to turn and send commands to se switch, to check power 
	command = "show power-over-ethernet brief"
	command_dict={'cmd': command}
	try:
		with requests.Session() as s:
			post_command = s.post(url + 'cli', data=json.dumps(command_dict), timeout=10)
		return 0,post_command
	except requests.exceptions.RequestException as e:
		return 1,str(e)



@csrf_exempt
def send_grid(request):

	code,info = refresh_grid()

	if code == 1:
		if request.is_ajax():
			return JsonResponse({"code": -1})
		return render(request, 'templates/Controller/error.html',{'error': "Can't refresh grid at the moment. Try again later.",'user': user})
	
	
	node_grid = grid

	if request.is_ajax():
		if request.method == 'GET':
			return JsonResponse(node_grid)
		else:
			dic=request.POST
		
			for key in dic:
				if key == 'id':
					node=dic[key]
				elif key == 'value':
					value=dic[key]
			
			
			(val,color,portId) = grid[int(node)]


			if value == 'OFF':
					#if value OFF turn on
					commands = "conf t\ninterface " + str(portId) + "\npower-over-ethernet\nwrite memory"

					#can't update database immediately, need to wait for node to go up
					code,post = send_commands(commands)

					if code == 1:
						return JsonResponse({'error': 'Connection to switch timed out. Could not turn on node!'})



					if post.status_code != 202:
						return JsonResponse({'error': 'commands not accepted.  Could not turn on node!'})

					return JsonResponse(node_grid)
			else:
				try:
					connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
					c=connection.cursor()
					
					#if value ON turn off
					commands = "conf t\ninterface " + str(portId) + "\nno power-over-ethernet\nwrite memory"

					query = "Update node Set value='OFF', dateOn = '0' where id=" + str(node) +";"
				
				
					code,post = send_commands(commands)


					if code == 1:
						
						c.close()
						connection.close()
						return JsonResponse({'error': 'Connection to switch timed out. Could not turn off node!'})

					if post.status_code != 202:
						c.close()
						connection.close()
						return JsonResponse({'error': 'commands not accepted.  Could not turn off node!'})


					#update value of node state in database
					c.execute(query)
					connection.commit()
					c.close()
					connection.close()

					count_alive[str(node)] = 0


					E_id,error = refresh_grid()
					if E_id == 1:
						return JsonResponse({'error': error})

				except sqlite3.Error as e:
					return JsonResponse({'error': str(e)})
					
				

				node_grid = grid

			
				
				return JsonResponse(node_grid)
			

	
	return render(request,'templates/Controller/config.html',{'node_grid':node_grid, 'user' : user, 'request':request_node, 'alert': alert})
	
	

def refresh_grid():
	try:	
		connection = sqlite3.connect("/home/ubuntu/apps/SwitchController/SwitchController/Controller/controller.db")
		c=connection.cursor()	
		c.execute("Select node_id, value, portId from node as N Join switch as S on N.id = S.node_id;")
		fetch= c.fetchall()
		for row in fetch:
			if str(row[1]) == 'ON':
				color='green'
			else:
				color = 'red'
			grid[row[0]] = (row[1],color,row[2])

		c.close()
		connection.close()
		return 0,grid
	except sqlite3.Error as e:
		return 1,str(e)


	
def send_commands(command):
	try:
		##sequence to turn and send commands to the switch, sequence of cli commands
		command_bytes = command.encode()
		command_base64 = base64.b64encode(command_bytes)
		command_dict={'cli_batch_base64_encoded': command_base64.decode('utf-8')}
		with requests.Session() as s:
			post_command = s.post(url + 'cli_batch', data=json.dumps(command_dict), timeout=10)
		return 0,post_command
	except requests.exceptions.RequestException as e:
		return 1,str(e)



def error_404(request,exception):
	return render(request, 'templates/Controller/notfound.html', {"error":"404 Page not found",'user' : user,'alert': alert, 'request':request_node})

def error_500(request):
	return render(request, 'templates/Controller/notfound.html', {"error": "Error 500",'user' : user,'alert': alert, 'request':request_node})
