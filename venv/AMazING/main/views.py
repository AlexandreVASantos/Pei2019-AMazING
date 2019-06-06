import requests
import re
import json
import string
from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login,authenticate,logout
from kafka import KafkaProducer
from kafka import KafkaConsumer
import sqlite3
import datetime
from json import dumps
from django.views.decorators.csrf import csrf_exempt
from background_task import background
from time import sleep


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
			print("('"+str(a)+"','"+str(b[0])+"','"+str(b[1])+"','"+str(b[2]) +"','"+str(b[3]) +"','"+str(b[4]) +"') values entered")
			cursor.execute("INSERT INTO Logs VALUES('"+ str(a)+"','"+str(b[0])+"','"+str(b[1])+"','"+str(b[2])+"','"+str(b[3])+"','"+str(b[4]) +"');")
			connection.commit()
		cursor.close()
		connection.close()
		sleep(2)


def auth(request):
	username = request.POST.get('email')
	password = request.POST.get('password')


	user = authenticate(username=username,password=password)
	if user is not None:
		login(request,user)
		refresh_grid()
		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {username: [curdate, 'Login','null' ,'null', 'null']}   #curdate= current date, data["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		return render(request,'main/NodeMenu.html',{'node_grid':grid})
	else:
		messages.warning(request,"Invalid credentials")
		system_messages.used = True
	return render(request,'main/login.html')

def AccessP(request):
	data=request.GET
	print(data)
	ident=data['id']
	return render(request,'main/AccessP.html',{'id':ident})

def home(request):
	return render(request, 'main/login.html')

def modBitrate(request):
	data=request.GET
	print(data)
	ident=data['id']
	return render(request, 'main/modBitrate.html',{'id':ident})

def about(request):
	return render(request, 'main/about.html')

def Logout(request):
	logout(request)
	return render(request, 'main/login.html')

def menu(request):	
	data = request.GET
	ident=""

	for key in data:
		if data[key] == "ON":
			ident = key 


	node_busy(request,{'id':ident});
	refresh_grid()
	return render(request, 'main/menu.html',{'id':ident})

def connection(request):
	data=request.GET
	print(data)
	ident=data['id']
	return render(request, 'main/connection.html',{'id':ident})

def NodeMenu(request):
	refresh_grid()
	return render(request, 'main/NodeMenu.html',{'node_grid':grid})

def main(request):
	return render(request, 'main/main.html')

def help(request):
	return render(request, 'main/help.html')

def stationPeer(request):
	data=request.GET
	print(data)
	ident=data['id']
	return render(request, 'main/stationPeer.html',{'id':ident})

def addrChange(request):
	data=request.GET
	ident=data['id']
	return render(request, 'main/addrChange.html',{'id':ident})

def setTxPower(request):
	data=request.GET
	print(data)
	ident=data['id']
	return render(request, 'main/SetTxPower.html',{'id':ident})

def postGetApIP(request):
	data=request.GET
	url = "http://10.110.1." + ident + ":5000/"
	for key in data:
		print(key)
		dic[key] = data[key]

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	updatedReqResp = req.json()
	return render(request,'main/menu.html',{'id':ident})

def postAccessP(request):
	data = request.GET
	ident=data['id']
	url = "http://10.110.1." + ident + ":5000/CreateAccessPoint"
	dic={}
	channel = int(data["Channel"])

	if(verify_Channel(request,channel) and verify_passw(request,data["APPW"]) and verify_Range(request,data["RangeStart"],data["RangeEnd"]) and verify_IP(request,data["RangeStart"]) and verify_IP(request,data["RangeEnd"]) and verify_IP(request,data["DFGateway"])):
		for key in data:
			print(key)
			dic[key] = data[key]

		if "id" in dic:
			del dic["id"]

		print(dic)
		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)
		updatedReqResp = req.json()

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {request.user.get_username() : [curdate, 'Create Access Point',ident ,'Channel: '+dic["Channel"]+', APPW: '+dic["APPW"]+', HW_Mode: '+dic["hw_mode"]+', RangeStart: ' +dic["RangeStart"]+ ', DFGateway: ' +dic["DFGateway"]+ ',APSSID: '+dic["APSSID"]+',Netmask: ' +dic["Netmask"]+',RangeEnd: ' +dic["RangeEnd"], 'Successful']}   #curdate= current date, data["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		return render(request, 'main/AccessP.html', {"flagAP":True,"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False,"flagMB":False,"req":updatedReqResp,'id':ident})#"req":updatedReqResp,
	
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	
	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Create Access Point',ident ,'Channel: '+dic["Channel"]+', APPW: '+dic["APPW"]+', HW_Mode: '+dic["hw_mode"]+', RangeStart: ' +dic["RangeStart"]+ ', DFGateway: ' +dic["DFGateway"]+ ',APSSID: '+dic["APSSID"]+',Netmask: ' +dic["Netmask"]+',RangeEnd: ' +dic["RangeEnd"], 'Failed']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)
	#print(req.json())
	return render(request,'main/AccessP.html',{'id':ident})

def postStopAccessPoint(request):
	data = request.GET
	ident=data['id']
	dic={}
	url = "http://10.110.1." +ident + ":5000/StopAccessPoint"

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	#print(req.json())

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Stop Access Point',ident ,'Channel: '+dic["Channel"]+', APPW: '+dic["APPW"]+', HW_Mode: '+dic["hw_mode"]+', RangeStart: ' +dic["RangeStart"]+ ', DFGateway: ' +dic["DFGateway"]+ ',APSSID: '+dic["APSSID"]+',Netmask: ' +dic["Netmask"]+',RangeEnd: ' +dic["RangeEnd"], 'Successful']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)
	return render(request,'main/menu.html',{'id':ident})	

def postDisconnect(request):
	data = request.GET
	ident=data['id']
	dic={}
	url = "http://10.110.1." + ident + ":5000/disconnect"

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	#print(req.json())

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Disconnect From Network',ident , 'null' , 'Successful']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	return render(request,'main/menu.html',{'id':ident})	

def postTurnOnNode(request):
	url = "http://192.168.85.228:8000/request/" 				
	#url = "http://httpbin.org/post"
	data=request.GET
	dic = {}
	nodes = ''

	for key in data:
		if data[key] == "OFF":
			dic["id"] = key 
	ident = dic["id"]

	#print(dic)
	dic["username"]=request.user.get_username();
	system_messages = messages.get_messages(request)
	messages.warning(request, 'Please wait a few minutes before configuring node')
	system_messages.used = True
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	updatedReqResp = req.json()
	print(updatedReqResp)
	node_up(request,dic)
	refresh_grid()

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Turn On Mode',nodes ,'null', 'null']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	return render(request,'main/NodeMenu.html',{'node_grid':grid,'id':ident})

def postScanning(request):
	data = request.GET
	ident=data['id']
	dic={}
	url = "http://10.110.1." + ident + ":5000/scan"

	if(verify_NetwC(request,data)):	
		
		for key in data:
			print(key)
			dic[key] = data[key]

		if "id" in dic:
			del dic["id"]

		print(dic)	
		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {request.user.get_username() : [curdate, 'Scan',ident ,dic["NetwC"], 'Successful']}   #curdate= current date, data["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		updatedReqResp = req.json()
		
		print(updatedReqResp)
		return render(request, 'main/menu.html', {"flagAP":False,"flagEL":False,"flagSC":True,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False,"req":updatedReqResp,'id':ident})

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Scan',ident ,data["NetwC"], 'Failed']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/menu.html',{'id':ident})

def postLinkStatus(request):
	data = request.GET
	ident=data['id']
	dic={}
	url = "http://10.110.1." + ident + ":5000/link"

	if(verify_NetwC(request,data)):	
		
		for key in data:
			#print(key)
			dic[key] = data[key]

		if "id" in dic:
			del dic["id"]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {request.user.get_username() : [curdate, 'Link Status',ident ,data["NetwC"], 'Successful']}   #curdate= current date, data["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		updatedReqResp=req.json()
		return render(request, 'main/menu.html', {"flagAP":False,"flagEL":False,"flagSC":False,"flagLS":True,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False,"req":updatedReqResp,'id':ident})

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	#print(data)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Link Status',ident ,data["NetwC"], 'Failed']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/menu.html',{'id':ident})

def postLocalWireless(request):
	data = request.GET
	ident=data['id']
	dic={}
	url = "http://10.110.1." + ident + ":5000/localwireless"
	#print(data)

	if(verify_NetwC(request,data)):	
		
		for key in data:
			#print(key)
			dic[key] = data[key]

		if "id" in dic:
			del dic["id"]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {request.user.get_username() : [curdate, 'Link Status',1 ,data["NetwC"], 'Successful']}   #curdate= current date, data["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		updatedReqResp=req.json()
		return render(request, 'main/menu.html', {"flagLC":True,"flagAP":False,"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False,"req":updatedReqResp,'id':ident})

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	#print(data)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Link Status',1 ,data["NetwC"], 'Failed']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/menu.html',{'id':ident})

def postIPChange(request):
	data = request.GET
	ident=data['id']
	url = "http://10.110.1." + ident + ":5000/changeIP"
	dic={}
	
	if(verify_IP(request,data["IP"]) and verify_netmask(request,data["Netmask"]) and not (len(data)==0)):	
		
		for key in data:
			dic[key] = data[key]

		#print(dic)
		if "id" in dic:
			del dic["id"]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		ddata = {request.user.get_username() : [curdate, 'Change Ip',ident ,'IP: '+data["IP"]+', NetwC: '+data["NetwC"], 'Successful']}   #curdate= current date, data["IP"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		updatedReqResp = req.json()
		#print(req.json())
		return render(request, 'main/addrChange.html', {"flagLC":False,"flagAP":False,"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":True,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False,"req":updatedReqResp,'id':ident})#"req":updatedReqResp
	
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Change Ip',ident ,'IP: '+data["IP"]+', NetwC: '+data["NetwC"], 'Failed']}   #curdate= current date, data["IP"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/addrChange.html',{'id':ident})

def postConnection(request):
	data = request.GET
	#print(data)
	ident=data['id']
	url = "http://10.110.1." + ident +":5000/connection"
	dic={}

	if(verify_NetwC(request,data) and not (len(data)==0)):	

			#print(data)
			for key in data:
				#print(key)
				dic[key] = data[key]

			if "id" in dic:
				del dic["id"]

			dataToSend = json.dumps(dic)
			headers = {'Content-Type': 'application/json'}
			req = requests.post(url,data=dataToSend, headers=headers)

			producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
			curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
			username='username'
			data = {request.user.get_username() : [curdate, 'Connection',ident ,'WEP: '+data["WEP"]+', NetwC: '+data["NetwC"]+', Frequency: '+data["Frequency"]+', SSID: '+data["SSID"], 'Successful']}   #curdate= current date, req.json() = output
			producer.send('numtest', value=data)
			sleep(2)

			updatedReqResp=req.json()
			return render(request, 'main/connection.html',{"flagLC":False,"flagAP":False,"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":True,"req":updatedReqResp,'id':ident})
			
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Connection',ident ,'null' 'Failed']}   #curdate= current date, req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/connection.html',{'id':ident})
	

def postStationStats(request):
	data = request.GET
	ident=data['id']
	url = "http://10.110.1." + ident +":5000/stationstats"
	dic={}


	if(verify_NetwC(request,data)):	
		
		for key in data:
			#print(key)
			dic[key] = data[key]

		if "id" in dic:
			del dic["id"]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)


		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {request.user.get_username() : [curdate, 'Station Stats',ident ,data["NetwC"], 'Successful']}   #curdate= current date, dic["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)


		#print(req.json())
		updatedReqResp = req.json()
		return render(request, 'main/menu.html', {"flagLC":False,"flagAP":False,"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":True,"flagSP":False,"flagTP":False,"flagC":False,"req":updatedReqResp,'id':ident})#"req":updatedReqResp,

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Station Stats',ident ,data["NetwC"], 'Failed']}   #curdate= current date, dic["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/menu.html',{'id':ident})

def postModBitrate(request):
	data = request.GET
	ident=data['id']
	url = "http://10.110.1." + ident +":5000/modtxhtmcsbitrates"
	dic={}

	if(verify_NetwC(request,data)):	
		for key in data:
			print(key)
			dic[key] = data[key]

		if "id" in dic:
			del dic["id"]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)
		updatedReqResp = req.json()

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {request.user.get_username() : [curdate, 'Modify Transmit Bitrate',ident ,'NetwC: '+dic["NetwC"]+', LBits: '+dic["Lbits"], 'Successful']}   #curdate= current date, data["Wlan"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)

		return render(request, 'main/modBitrate.html', {"flagLC":False,"flagAP":False,"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False,"flagMB":True,"req":updatedReqResp,'id':ident})#"req":updatedReqResp,

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	#print(req.json())

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Modify Transmit Bitrate',ident ,'NetwC: '+dic["NetwC"]+', LBits: '+dic["Lbits"], 'Failed']}   #curdate= current date, data["Wlan"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	return render(request,'main/modBitrate.html',{'id':ident})		


def postStationPeer(request):
	data = request.GET
	ident=data['id']
	url = "http://10.110.1." + ident + ":5000/stationpeerstats"
	mac=data["MAC"]
	dic={}

	if not (len(data)==0):
		if(verify_NetwC(request,data) and verify_mac(request,mac)):
				
			
			for key in data:
				dic[key] = data[key]

			#print(dic)	

			if "id" in dic:
				del dic["id"]

			dataToSend = json.dumps(dic)
			headers = {'Content-Type': 'application/json'}
			req = requests.post(url,data=dataToSend, headers=headers)

			producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
			curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
			username='username'
			data = {request.user.get_username() : [curdate, 'Station Peer',ident ,'NetwC: '+data["NetwC"]+', MAC: '+data["MAC"], 'Successful']}  #curdate= current date, mac=input , req.json() = output
			producer.send('numtest', value=data)
			sleep(2)

			updatedReqResp=req.json()
			return render(request, 'main/stationPeer.html',{"flagLC":False,"flagAP":False,"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":True,"flagTP":False,"flagC":False,"req":updatedReqResp,'id':ident})

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Station Peer',ident ,'NetwC: '+data["NetwC"]+', MAC: '+data["MAC"], 'Failed']}   #curdate= current date, mac=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/stationPeer.html',{'id':ident})
	
	

def postTxPower(request):
	data = request.GET
	ident=data['id']
	url = "http://10.110.1." + ident + ":5000/settingtxpowerdev"
	dic={}
	
	if(verify_NetwC(request,data) and not (len(data)==0)):	
		
		for key in data:
			#print(key)
			dic[key] = data[key]

		if "id" in dic:
			del dic["id"]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)

		producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
		curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
		username='username'
		data = {request.user.get_username() : [curdate, 'Tx Power',ident ,'TxPower: '+dic["TxPower"]+', NetwC: '+data["NetwC"], 'Successful']}   #curdate= current date, data["NetwC"]=input , req.json() = output
		producer.send('numtest', value=data)
		sleep(2)
		updatedReqResp=req.json()
		return render(request, 'main/SetTxPower.html',{"flagLC":False,"flagAP":False,"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":True,"flagC":False,"req":updatedReqResp,'id':ident})


	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	curdate = datetime.datetime.today().strftime('[%d/%B/%Y %H:%M:%S]')
	username='username'
	data = {request.user.get_username() : [curdate, 'Tx Power',ident ,'TxPower: '+dic["TxPower"]+', NetwC: '+data["NetwC"], 'Failed']}   #curdate= current date, data["NetwC"]=input , req.json() = output
	producer.send('numtest', value=data)
	sleep(2)

	#print(req.json())
	return render(request,'main/SetTxPower.html',{'id':ident})




@csrf_exempt
def compare_owner(request):
	dic=request.GET
	ident = dic["id"]
	print("id",ident)
	ownerList = node_owner(request,dic)
	owner=ownerList[0]

	refresh_grid()
	if owner[0] == request.user.get_username():
		return render(request,'main/menu.html',{"id":ident})
	else:
		return render(request,'main/NodeMenu.html',{"node_grid":grid,"id":ident})


@csrf_exempt
def node_owner(request,dic):
	try:
		node = dic["id"]
		print(node)
		connection = sqlite3.connect("/home/santananas/Desktop/sitePei/venv/AMazING/NodeDB.db")
		c=connection.cursor()

		query = "Select owner From node where id='"+ str(node) +"';"
		#Only at this time we can update the value of the node in the database
		
		c.execute(query)
		fetch= c.fetchall()
		connection.close()
		
		return fetch

	except sqlite3.Error as e:			
		return render(request, 'main/NodeMenu.html', {'message' : 'database error'})

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
		user=request.user.get_username()
		
		node = dic["id"]
		connection = sqlite3.connect("/home/santananas/Desktop/sitePei/venv/AMazING/NodeDB.db")
		c=connection.cursor()

		query = "Update node Set value='BUSY', owner='" + str(user) + "' where id="+ str(node) +";"
		#Only at this time we can update the value of the node in the database
		#print(query)
		c.execute(query)
		
		connection.commit()
		
		connection.close()
		
		return render(request, 'main/menu.html', {'message' : 0})

	except sqlite3.Error as e:			
		return render(request, 'main/NodeMenu.html', {'message' : 'database error'})

@csrf_exempt
def send_grid(request):		#esta funcao tem que ser alterada (grid)
	
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
	

def get_IP(NOwner,NId):
	try:	
		connection = sqlite3.connect("/home/santananas/Desktop/sitePei/venv/AMazING/NodeDB.db")
		c=connection.cursor()	
		c.execute("Select IP from node where owner="+ str(NOwner) +",id="+ str(NId) +";")
		fetch= c.fetchall()
		connection.close()
		print("ip;",fetch)
		return fetch
	except sqlite3.Error as e:
		return 1,str(e)

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
		messages.warning(request, 'Please select Wlan.')
		system_messages.used = True
		return 0
	return 1

def verify_Range(request,rangeStart,rangeStop):
	system_messages = messages.get_messages(request)
	RSta = rangeStart.split('.')
	RSto = rangeStop.split('.')
	print("RSta",RSta)
	print("RSto",RSto)

	if len(RSta) is not 4 :
		messages.warning(request, 'Please insert a valid IP on range Start.')
		system_messages.used = True
		return 0
	if len(RSto) is not 4 :
		messages.warning(request, 'Please insert a valid IP on range Stop.')
		system_messages.used = True
		return 0

	if RSta[0] <= RSto[0] and RSta[1] <= RSto[1] and RSta[2] <= RSto[2] and RSta[3] <= RSto[3]:
		return 1
	
	messages.warning(request, 'Please insert a valid IP range.')
	system_messages.used = True
	return 0

def verify_Channel(request,channel):
	system_messages = messages.get_messages(request)
	print(channel)
	if channel not in range(0,12):
		messages.warning(request, 'Please insert a valid Channel (1-11).')
		system_messages.used = True
		return 0
	return 1

def verify_passw(request,password):
	system_messages = messages.get_messages(request)
	if len(password) < 8:
		messages.warning(request, 'Please insert a valid Password (8 or more characters).')
		system_messages.used = True
		return 0
	return 1