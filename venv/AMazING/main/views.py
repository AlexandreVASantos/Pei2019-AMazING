import requests
import json
from django.shortcuts import render
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
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	
	#dic = {"data":"123"}
	dic={}
	for key in data:
		dic[key] = data[key]

		
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request,'main/menu.html', {"flagEL":True,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False})

def postScanning(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	
	#dic = {"data":"123"}
	dic={}
	for key in data:
		dic[key] = data[key]

		
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request, 'main/menu.html', {"flagEL":False,"flagSC":True,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False})

def postLinkStatus(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	
	#dic = {"data":"123"}
	dic={}
	for key in data:
		dic[key] = data[key]

		
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request, 'main/menu.html', {"flagEL":False,"flagSC":False,"flagLS":True,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False})


def postIPChange(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	
	#dic = {"data":"123"}
	dic={}
	for key in data:
		dic[key] = data[key]

		
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request, 'main/menu.html', {"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":True,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":False})

def postConnection(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/connect"
	data = request.GET
	#print(data)
	#dic = {"data":"123"}
	#dic = {"data":"123"}
	dic={}
	for key in data:
		dic[key] = data[key]

		
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request, 'main/connection.html',{"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":False,"flagC":True})

def postStationStats(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET 										#########NOT WORKING request.GET vazio 
					
	#dic = {"data":"123"}
	#dic = {"data":"123"}
	dic={}
	for key in data:
		dic[key] = data[key]

		
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request, 'main/menu.html', {"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":True,"flagSP":False,"flagTP":False,"flagC":False})

def postStationPeer(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	print(data)
	#dic = {"data":"123"}

	dic={}
	for key in data:
		dic[key] = data[key]

		
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request, 'main/stationPeer.html',{"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":True,"flagTP":False,"flagC":False})

def postTxPower(request):
	url = "http://httpbin.org/post"
	#url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	
	#dic = {"data":"123"}
	dic={}
	for key in data:
		dic[key] = data[key]

		
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request, 'main/menu.html',{"flagEL":False,"flagSC":False,"flagLS":False,"flagIPC":False,"flagSS":False,"flagSP":False,"flagTP":True,"flagC":False})


def get(request):
	#producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	url = "http://192.168.0.25:5000/changeIP"
	headers = {'Content-Type': 'application/json'}
	req = requests.get(url, headers=headers)
	print(req.json())
	#curdate = datetime.datetime.today().strftime('%B %d, %Y - %H:%M:%S')
	#data = {'username' : [curdate, url[:27],value, req.json()]}   #curdate= current date, url[:27]= function name, value=input , req.json() = output
    #producer.send('numtest', value=data)
	return render(request, 'main/menu.html')

def verify_mac(mac_address):
	if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_address.lower()):
		return 1
	return 0

def verify_IP(IP_address):
	a = IP_address.split('.')
	if len(a) != 4:
		return 0
	for x in a:
		if not x.isdigit():
			return 0
		i = int(x)
		if i < 0 or i > 255:
			return 0
	return 1

def verify_freq(freq):
	if freq.isdigit():
		return 1
	return 0

def verify_wep(wep, size):
	if re.match("[0-9a-f]*",wep.lower()) and len(wep)==(size/4):
		return 1
	return 0	
