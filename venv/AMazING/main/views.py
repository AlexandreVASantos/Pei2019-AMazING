import requests
import json
from django.shortcuts import render
from django.http import HttpResponse
from kafka import KafkaProducer

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



def post(request):
	#url = "http://httpbin.org/post"
	url = "http://192.168.0.25:5000/changeIP"
	data = request.GET
	
	#dic = {"data":"123"}
	for key in data:
		node=key
		value=data[key]

	
	dic = {node:value}
	dataToSend = json.dumps(dic)
	headers = {'Content-Type': 'application/json'}
	req = requests.post(url,data=dataToSend, headers=headers)
	print(req.json())
	return render(request, 'main/menu.html')

def get(request):
	#producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: dumps(x).encode('utf-8'))
	url = "http://192.168.0.25:5000/changeIP"
	headers = {'Content-Type': 'application/json'}
	req = requests.get(url, headers=headers)
	print(req.json())
	#data = {'username' : [url[:27],value, req.json()]}   #url[:27]= function name, value=input , req.json() = output
    #producer.send('numtest', value=data)
	return render(request, 'main/menu.html')	