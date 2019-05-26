import requests
import re
import json
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from kafka import KafkaProducer
from kafka import KafkaConsumer
import sqlite3
import datetime
from json import dumps
from background_task import background
from time import sleep
from django.views.decorators.csrf import csrf_exempt

grid={}

@background(schedule=1)
def consumer():
	consumer = KafkaConsumer('numtest', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=True, group_id='my_group', value_deserializer=lambda x:json.loads(x.decode('utf-8')))
	count = 0
	for message in consumer:
		count = count+1
		connection = sqlite3.connect("main/Logs/Logs.db")
		cursor = connection.cursor()
		message = message.value
		for (a,b) in message.items():
			print("("+str(a)+"','"+str(b[0])+"','"+str(b[1])+"','"+str(b[2]) +"','"+str(b[3]) +"','"+str(b[4]) +") values entered")
			cursor.execute("INSERT INTO Logs VALUES('"+ str(a)+"','"+str(b[0])+"','"+str(b[1])+"','"+str(b[2])+"','"+str(b[3])+"','"+str(b[4]) +"');")
			connection.commit()
		cursor.close()
		connection.close()
		sleep(2)


def auth(request):
	username = request.POST.get('email')
	password = request.POST.get('password')


	user = authenticate(username=username,password=password)
	print(user)
	if user is not None:
		print("ola")
		login(request,user)

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {'User: '+user : [curdate, 'Login','null' ,'null', 'null']}   #curdate= current date, data["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		return redirect('NodeMenu/')
	else:
		messages.warning(request,"Invalid credentials")
	print("adeus")
	return render(request,'main/login.html')

def AccessP(request):
	return render(request,'main/AccessP.html')

def home(request):
	return render(request, 'main/login.html')

def modBitrate(request):
	return render(request, 'main/modBitrate.html')

def about(request):
	return render(request, 'main/about.html')

def menu(request):
	return render(request, 'main/menu.html')

def connection(request):
	return render(request, 'main/connection.html')

def NodeMenu(request):
	return render(request, 'main/NodeMenu.html')

def main(request):
	return render(request, 'main/main.html')

def help(request):
	return render(request, 'main/help.html')

def stationPeer(request):
	return render(request, 'main/stationPeer.html')

def addrChange(request):
	return render(request, 'main/addrChange.html')

def setTxPower(request):
	return render(request, 'main/SetTxPower.html')

def postAccessP(request):
	url = "http://httpbin.org/post"
	data = request.GET
	dic={}

	if 1:
	#if(verify_Channel(request,data["Channel"]) and verify_Range(request,data["RangeStart"],data["RangeEnd"]) and verify_IP(request,data["RangeStart"]) and verify_IP(request,data["RangeEnd"]) and verify_IP(request,data["DFGateway"])):
		for key in data:
			print(key)
			dic[key] = data[key]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)
		updatedReqResp = req.json()

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {'User: '+username : [curdate, 'Create Access Point','1' ,'Channel: '+dic["Channel"]+', APPW: '+dic["APPW"]+', HW_Mode: '+dic["HW_Mode"]+', RangeStart: ' +dic["RangeStart"]+ ', DFGateway: ' +dic["DFGateway"]+ ',APSSID: '+dic["APSSID"]+',Netmask: ' +dic["Netmask"]+',RangeEnd: ' +dic["RangeEnd"], 'output']}   #curdate= current date, data["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		return render(request, 'main/AccessP.html', {"flagEL":False,"flagSC":True,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False,"flagMB":False,"req":updatedReqResp})
	
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request,'main/AccessP.html')

def postDisconnect(request):
	#url = "http://10.42.0.95:5000/disconnect"
	url = "http://httpbin.org/post"
	data = request.GET
	dic={}

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {'User: '+username : [curdate, 'Disconnect From Network','1' , 'null' , 'output']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	return render(request,'main/menu.html')	

def postTurnOnNode(request):
	#url = "http://" 				falar alex
	url = "http://httpbin.org/post"
	data=request.GET
	dic = {}
	nodes = ''

	for key in data:
		if data[key] == "OFF":
			dic["id"] = key 
			nodes += ' key'


	#print(dic)
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	updatedReqResp = req.json()
	#print(updatedReqResp)
	node_up(request,dic)
	refresh_grid()

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {'User: '+username : [curdate, 'Turn On Mode',nodes ,'null', 'null']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	return render(request,'main/NodeMenu.html',{'node_grid':grid})

def postScanning(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	dic={}
	#print(data)

	if(verify_NetwC(request,data)):	
		
		for key in data:
			#print(key)
			dic[key] = data[key]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {'User: '+username : [curdate, 'Scan','1' ,dic["NetwC"], 'output']}   #curdate= current date, data["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		#print(req.json())
		return render(request, 'main/menu.html', {"flagEL":False,"flagSC":True,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False})

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {'User: '+username : [curdate, 'Scan','1' ,data["NetwC"], 'output']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/menu.html')	

def postLinkStatus(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	dic={}
	#print(data)

	if(verify_NetwC(request,data)):	
		
		for key in data:
			#print(key)
			dic[key] = data[key]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {'User: '+username : [curdate, 'Link Status','1' ,data["NetwC"], 'output']}   #curdate= current date, data["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		#print(req.json())
		return render(request, 'main/menu.html', {"flagEL":False,"flagSC":False,"flagLS":True,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False})

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	#print(data)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {'User: '+username : [curdate, 'Link Status','1' ,data["NetwC"], 'output']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/menu.html')



def postIPChange(request):
	url = "http://httpbin.org/post"
	#url = "http://10.42.0.2:5000/changeIP"
	data = request.GET
	dic={}
	
	if(verify_IP(request,data["IP"]) and verify_netmask(request,data["Netmask"]) and not (len(data)==0)):	
		
		for key in data:
			dic[key] = data[key]

		#print(dic)
		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {'User: '+username : [curdate, 'Change Ip','1' ,'IP: '+data["IP"]+', NetwC: '+data["NetwC"], 'output']}   #curdate= current date, data["IP"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		updatedReqResp = req.json()
		#print(req.json())
		return render(request, 'main/menu.html', {"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":True,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False,"req":updatedReqResp})
	
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {'User: '+username : [curdate, 'Change Ip','1' ,'IP: '+data["IP"]+', NetwC: '+data["NetwC"], 'output']}   #curdate= current date, data["IP"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/addrChange.html')

def postConnection(request):
	url = "http://httpbin.org/post"
	#url = "http://10.42.0.2:5000/connection"
	data = request.GET
	dic={}
	#print(data)
	#dic = {"data":"123"}
	#dic = {"data":"123"}

	if(verify_NetwC(request,data) and not (len(data)==0)):	
			if data["Frequency"]:
				if not verify_freq(request,data["Frequency"]):
					dataToSend = json.dumps(dic)
					headers = {'Content-Type': 'application/json'}
					req = requests.post(url,data=dataToSend, headers=headers)
					#print(req.json())
					return render(request,'main/connection.html')

			if data["WEP"]:
				if not verify_wep(request,data["WEP"]):
					dataToSend = json.dumps(dic)
					headers = {'Content-Type': 'application/json'}
					req = requests.post(url,data=dataToSend, headers=headers)
					#print(req.json())
					return render(request,'main/connection.html')

			#print(data)
			for key in data:
				#print(key)
				dic[key] = data[key]

			dataToSend = json.dumps(dic)
			headers = {'Content-Type': 'application/json'}
			req = requests.post(url,data=dataToSend, headers=headers)

			producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
			curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
			username='username'
			data = {'User: '+username : [curdate, 'Connection','1' ,'WEP: '+data["WEP"]+', NetwC: '+data["NetwC"]+', Frequency: '+data["Frequency"]+', SSID: '+data["SSID"],'output']}   #curdate= current date, req.json() = output
			producer.send('numtest', value=data)
			sleep(2)

			#print(req.json())
			return render(request, 'main/connection.html',{"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":True})
			
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {'User: '+username : [curdate, 'Connection','1' ,'null','output']}   #curdate= current date, req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/connection.html')
	

def postStationStats(request):
	url = "http://httpbin.org/post"
	#url = "http://10.42.0.2:5000/stationstats"
	data = request.GET
	dic={}
	#print(data)

	if(verify_NetwC(request,data)):	
		
		for key in data:
			#print(key)
			dic[key] = data[key]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)


		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {'User: '+username : [curdate, 'Station Stats','1' ,data["NetwC"], 'output']}   #curdate= current date, dic["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)


		#print(req.json())
		updatedReqResp = req.json()
		return render(request, 'main/menu.html', {"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":True,"flagSP":False,"flagTP":False,"flagC":False,"req":updatedReqResp})

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {'User: '+username : [curdate, 'Station Stats','1' ,data["NetwC"], 'output']}   #curdate= current date, dic["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/menu.html')

def postModBitrate(request):
	url = "http://httpbin.org/post"					
	#url = "http://10.42.0.95:5000/stationstats"
	data = request.GET
	dic={}
	#print(data)

	if(verify_NetwC(request,data)):	
		for key in data:
			print(key)
			dic[key] = data[key]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)
		updatedReqResp = req.json()

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {'User: '+username : [curdate, 'Modify Transmit Bitrate','1' ,'NetwC: '+dic["NetwC"]+', LBits: '+dic["Lbits"], 'output']}   #curdate= current date, data["Wlan"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		return render(request, 'main/modBitrate.html', {"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False,"flagMB":True,"req":updatedReqResp})

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {'User: '+username : [curdate, 'Modify Transmit Bitrate','1' ,'NetwC: '+dic["NetwC"]+', LBits: '+dic["Lbits"], 'output']}   #curdate= current date, data["Wlan"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	return render(request,'main/menu.html')	


def postStationPeer(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	#print(data)
	#dic = {"data":"123"}
	mac=data["MAC"]
	dic={}

	if not (len(data)==0):
		if(verify_NetwC(request,data) and verify_mac(request,mac)):
				
			
			for key in data:
				dic[key] = data[key]

			#print(dic)	

			dataToSend = json.dumps(dic)
			headers = {'Content-Type': 'application/json'}
			req = requests.post(url,data=dataToSend, headers=headers)

			producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
			curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
			username='username'
			data = {'User: '+username : [curdate, 'Station Peer','1' ,'NetwC: '+data["NetwC"]+', MAC: '+data["MAC"], 'output']}   #curdate= current date, mac=input , req.json() = output
			producer.send('numtest', value=data)
			sleep(2)

			#print(req.json())
			return render(request, 'main/stationPeer.html',{"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":True,"flagTP":False,"flagC":False})

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {'User: '+username : [curdate, 'Station Peer','1' ,'NetwC: '+data["NetwC"]+', MAC: '+data["MAC"], 'output']}   #curdate= current date, mac=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/stationPeer.html')
	
	

def postTxPower(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/settingtxpowerdev"
	data = request.GET
	dic={}
	#print(data)
	#dic = {"data":"123"}
	#dic = {"data":"123"}
	
	if(verify_NetwC(request,data) and not (len(data)==0)):	
		
		for key in data:
			#print(key)
			dic[key] = data[key]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {'User: '+username : [curdate, 'Tx Power','1' ,'TxPower: '+dic["TxPower"]+', NetwC: '+data["NetwC"], 'output']}   #curdate= current date, data["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)
		
		return render(request, 'main/SetTxPower.html',{"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":True,"flagC":False})


	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {'User: '+username : [curdate, 'Tx Power','1' ,'TxPower: '+dic["TxPower"]+', NetwC: '+data["NetwC"], 'output']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/SetTxPower.html')


def get(request):
	url = "http://192.168.0.25:5000/changeIP"
	#producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	url = "http://10.42.0.2:5000/getlist"

	headers = {'Content-Type': 'application/json'}
	req = requests.get(url, headers=headers)
	#print(req.json())
	return render(request, 'main/menu.html')

@csrf_exempt
def node_up(request,dic):
	try:
		node = dic["id"]
		connection = sqlite3.connect("/home/santananas/Desktop/sitePei/venv/AMazING/NodeDB.db")
		c=connection.cursor()

		query = "Update node Set value='ON' where id="+ str(node) +";"
		#Only at this time we can update the value of the node in the database
		
		c.execute(query)
		connection.commit()
		connection.close()
		
		return render(request, 'main/menu.html', {'message' : 0})

	except sqlite3.Error as e:			
		return render(request, 'main/NodeMenu.html', {'message' : 'database error'})


@csrf_exempt
def node_busy(request,dic):
	try:
		node = dic["id"]
		connection = sqlite3.connect("/home/santananas/Desktop/sitePei/venv/AMazING/NodeDB.db")
		c=connection.cursor()

		query = "Update node Set value='BUSY' where id="+ str(node) +";"
		#Only at this time we can update the value of the node in the database
		
		c.execute(query)
		connection.commit()
		connection.close()
		
		return render(request, 'main/menu.html', {'message' : 0})

	except sqlite3.Error as e:			
		return render(request, 'main/NodeMenu.html', {'message' : 'database error'})


@csrf_exempt
def send_grid(request):
	
	code = refresh_grid()

	if code[0] == 1:
		return render(request, 'main/NodeMenu.html',{'error': "Can't refresh grid at the moment. Try again later.",'user': user, 'alert':alert})
	
	##use this block if a user login is added to the switch
	#sess = requests.Session()
	#req = sess.post(url + 'login-sessions',data={},timeout=1)
	#cookie_response = req.json()['cookie']
	#cookie = {'cookie : cookie_response'}
	#if req.status_code != 201:
	#	return render(request, 'Controller/error.html', {'error': 'could not connect to the Switch'})

	
	node_grid = grid

	if request.method == 'GET':
		return JsonResponse(node_grid)
	else:
		dic=request.POST
	
		for key in dic:
			if key == 'id':
				node=dic[key]
			elif key == 'value':
				value=dic[key]

			print(node)
			print(value)
			
			(val,color,portId) = grid[int(node)]

			# if value == 'OFF':
			# 		#if value OFF turn on
			# 		commands = "interface" + str(portId) + "\npower-over-ethernet\n"

			# 		#can't update database immediately, need to wait for node to go up
			# 		post = send_commands(commands)

			# 		if post.status_code != 202:
			# 			return render(request, 'Controller/error.html', {'error': 'commands not accepted'})
			# else:
			try:
				connection = sqlite3.connect("/home/santananas/Desktop/sitePei/venv/AMazING/NodeDB.db")
				c=connection.cursor()
				
				#if value ON turn off
				commands = "interface" + str(portId) + "\nno power-over-ethernet\n"

				query = "Update node Set value='OFF', dateOn = '0' where id=" + str(node) +";"
			
			
				# post = send_commands(commands)
				# if post.status_code != 202:
				# 	return render(request, 'Controller/error.html', {'error': 'commands not accepted'})



				# verify_response = post.json()['result_base64_encoded']
				# decoded_r = base64.b64decode(verify_response).decode('utf-8')
				# print(decoded_r)
				#update value of node state in database
				c.execute(query)
				connection.commit()
				connection.close()


				E_id,error = refresh_grid()
				if E_id == 1:
					return render(request, 'main/NodeMenu.html', {'error': error,'user' : user})

			except sqlite3.Error as e:
				return render(request, 'main/NodeMenu.html', {'error': str(e),'user' : user})
				
			

			node_grid = grid

		
			print ('asdakjsdhiadhah')
			return JsonResponse(node_grid)
		

	
	return render(request,'main/NodeMenu.html',{'node_grid':node_grid, 'user' : user, 'alert': alert})
	
	

def refresh_grid():
	try:	
		connection = sqlite3.connect("/home/santananas/Desktop/sitePei/venv/AMazING/NodeDB.db")
		c=connection.cursor()	
		c.execute("Select id, value from node;")
		fetch= c.fetchall()
		for row in fetch:
			if str(row[1]) == 'ON':
				color='green'
			else:
				color = 'red'
			grid[row[0]] = (row[1],color)
		connection.close()
		return 0,grid
	except sqlite3.Error as e:
		return 1,str(e)


def verify_netmask(request,netmask):
	system_messages = messages.get_messages(request)
	if netmask == '':
		return 1

	octets = netmask.split(".")
	if len(octets) == 4 and all(o.isdigit() and 0 <= int(o) < 256 for o in octets):
		return 1
	messages.warning(request, 'Please enter a valid Netmask address.')
	system_messages.used = True
	return 0


def verify_mac(request,mac_address):
	system_messages = messages.get_messages(request)
	if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()):
		return 1
	messages.warning(request, 'Please enter a valid Mac address.')
	system_messages.used = True
	return 0

def verify_IP(request,IP_address):
	system_messages = messages.get_messages(request)
	a = IP_address.split('.')
	if len(a) is not 4:
		messages.warning(request, 'Please insert a valid IP.')
		system_messages.used = True
		return 0
	for x in a:
		if not x.isdigit():
			messages.warning(request, 'Please insert a valid IP.')
			system_messages.used = True
			return 0
		i = int(x)
		if i < 0 or i > 255:
			messages.warning(request, 'Please insert a valid IP.')
			system_messages.used = True
			return 0
	return 1

def verify_freq(request,freq):
	system_messages = messages.get_messages(request)
	if freq.isdigit():
		return 1
	freqsplit = freq.split('.')
	for a in freqsplit:
		if not a.isdigit():
			messages.warning(request, 'Please insert a valid Frequency.')
			system_messages.used = True
			return 0
	return 1

def verify_wep(request,wep):
	system_messages = messages.get_messages(request)
	if re.match("[0-9a-f]*",wep.lower()):
		return 1
	messages.warning(request, 'Please insert a valid WEP Key.')
	system_messages.used = True
	return 0	

def verify_NetwC(request,dic):
	system_messages = messages.get_messages(request)
	if "NetwC" not in dic:
		messages.warning(request, 'Please select NetwC.')
		system_messages.used = True
		return 0
	return 1