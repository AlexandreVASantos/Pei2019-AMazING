import requests
import re
import json
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from kafka import KafkaProducer
import datetime


def home(request):
	return render(request, 'main/login.html')

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


def postEventListening(request):
	#url = "http://httpbin.org/post"
	url = "http://10.42.0.2:5000/event"
	data = request.GET
	
	dic = {"data":"123"}
	# dic={}
	# for key in data:
	# 	dic[key] = data[key]

		
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	updatedReqResp = req.json()
	return render(request,'main/menu.html', {"flagEL":True,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False,"req":updatedReqResp['data']})

def postScanning(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	dic={}
	#print(data)

	if(verify_Wlan(request,data)):	
		
		for key in data:
			print(key)
			dic[key] = data[key]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)
		print(req.json())
		return render(request, 'main/menu.html', {"flagEL":False,"flagSC":True,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False})

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request,'main/menu.html')	

def postLinkStatus(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	dic={}
	#print(data)

	if(verify_Wlan(request,data)):	
		
		for key in data:
			print(key)
			dic[key] = data[key]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)
		print(req.json())
		return render(request, 'main/menu.html', {"flagEL":False,"flagSC":False,"flagLS":True,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False})
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request,'main/menu.html')



def postIPChange(request):
	#url = "http://httpbin.org/post"
	url = "http://10.42.0.2:5000/changeIP"
	data = request.GET
	dic={}
	
	print(verify_IP(request,data["IP"]))
	if(verify_IP(request,data["IP"]) and not (len(data)==0)):	
		
		for key in data:
			print(key)
			dic[key] = data[key]

		print(dic)
		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)
		updatedReqResp = req.json()
		#print(req.json())
		return render(request, 'main/menu.html', {"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":True,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False,"req":updatedReqResp})
	
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request,'main/addrChange.html')

def postConnection(request):
	#url = "http://httpbin.org/post"
	url = "http://10.42.0.2:5000/connection"
	data = request.GET
	dic={}
	#print(data)
	#dic = {"data":"123"}
	#dic = {"data":"123"}

	if(verify_Wlan(request,data) and not (len(data)==0)):	
			if data["Frequency"]:
				if not verify_freq(request,data["Frequency"]):
					dataToSend = json.dumps(dic)
					headers = {'Content-Type': 'application/json'}
					req = requests.post(url,data=dataToSend, headers=headers)
					print(req.json())
					return render(request,'main/connection.html')

			if data["WEP"]:
				if not verify_wep(request,data["WEP"]):
					dataToSend = json.dumps(dic)
					headers = {'Content-Type': 'application/json'}
					req = requests.post(url,data=dataToSend, headers=headers)
					print(req.json())
					return render(request,'main/connection.html')

			print(verify_Wlan(request,data))
			for key in data:
				print(key)
				dic[key] = data[key]

			dataToSend = json.dumps(dic)
			headers = {'Content-Type': 'application/json'}
			req = requests.post(url,data=dataToSend, headers=headers)
			print(req.json())
			return render(request, 'main/connection.html',{"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":True})
			
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request,'main/connection.html')
	

def postStationStats(request):
	#url = "http://httpbin.org/post"
	url = "http://10.42.0.2:5000/stationstats"
	data = request.GET
	dic={}
	#print(data)

	if(verify_Wlan(request,data)):	
		
		for key in data:
			print(key)
			dic[key] = data[key]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)
		#print(req.json())
		updatedReqResp = req.json()
		return render(request, 'main/menu.html', {"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":True,"flagSP":False,"flagTP":False,"flagC":False,"req":updatedReqResp})
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
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
		if(verify_Wlan(request,data) and verify_mac(request,mac)):
				
			
			for key in data:
				dic[key] = data[key]

			print(dic)	
			dataToSend = json.dumps(dic)
			headers = {'Content-Type': 'application/json'}
			req = requests.post(url,data=dataToSend, headers=headers)
			print(req.json())
			return render(request, 'main/stationPeer.html',{"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":True,"flagTP":False,"flagC":False})

	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request,'main/stationPeer.html')
	
	

def postTxPower(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	dic={}
	#print(data)
	#dic = {"data":"123"}
	#dic = {"data":"123"}
	
	if(verify_Wlan(request,data) and not (len(data)==0)):	
		
		for key in data:
			print(key)
			dic[key] = data[key]

		dataToSend = json.dumps(dic)
		headers = {'Content-Type': 'application/json'}
		req = requests.post(url,data=dataToSend, headers=headers)
		print(req.json())
		return render(request, 'main/SetTxPower.html',{"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":True,"flagC":False})
	
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request,'main/SetTxPower.html')


def get(request):
	#producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	url = "http://10.42.0.2:5000/getlist"
	headers = {'Content-Type': 'application/json'}
	req = requests.get(url, headers=headers)
	print(req.json())
	#curdate = datetime.datetime.today().strftime('%B %d, %Y - %H:%M:%S')
	#data = {'username' : [curdate, url[:27],value, req.json()]}   #curdate= current date, url[:27]= function name, value=input , req.json() = output
    #producer.send('numtest', value=data)
	return render(request, 'main/menu.html')

def verify_mac(request,mac_address):
	if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()):
		return 1
	messages.warning(request, 'Please enter a valid Mac address.')
	return 0

def verify_IP(request,IP_address):
	a = IP_address.split('.')
	if len(a) is not 4:
		messages.warning(request, 'Please insert a valid IP.')
		return 0
	for x in a:
		if not x.isdigit():
			messages.warning(request, 'Please insert a valid IP.')
			return 0
		i = int(x)
		if i < 0 or i > 255:
			messages.warning(request, 'Please insert a valid IP.')
			return 0
	return 1

def verify_freq(request,freq):
	if freq.isdigit():
		return 1
	messages.warning(request, 'Please insert a valid Frequency.')
	return 0

def verify_wep(request,wep, size):
	if re.match("[0-9a-f]*",wep.lower()) and len(wep)==(size/4):
		return 1
	messages.warning(request, 'Please insert a valid WEP Key.')
	return 0	

def verify_Wlan(request,dic):
	if "Wlan" not in dic:
		messages.warning(request, 'Please select Wlan.')
		return 0
	return 1