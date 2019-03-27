from django.shortcuts import render
from rest_framework import viewsets
import json
import requests

grid={'1':'OFF','2':'OFF','3':'OFF','4':'OFF','5':'OFF','6':'OFF','7':'OFF','8':'OFF','9':'OFF','10':'OFF','11':'OFF','12':'OFF','13':'OFF','14':'OFF','15':'OFF','16':'OFF','17':'OFF','18':'OFF','19':'OFF','20':'OFF','21':'OFF','22':'OFF','23':'OFF','24':'OFF'}
# Create your views here.
def home(request):
	return render(request,'Controller/home.html')
def send_grid(request):
	return render(request,'Controller/config.html',grid)

def send_shit(request):
	
		#url = 'http://192.1.1.1/connection'
		url = "http://httpbin.org/post"
		#data = {"SSID":"foo","Frequency":"1234","WEP":"1234123asdgwer"}
		data = {"data":"123"}
		dic=request.GET
		for key in dic:
			node=key
			value=dic[key]
		
		
		print(value)
		if value == 'OFF':
			print('dnfkjsfjksdjfsnfdgkdfgkdkjfsdkjfbsdk')
		#turn on
			grid[node] ="ON"
		else:
		#turn off
			print("blablablabla")
			grid[node] ="OFF"
		#
		print(grid['1'])
		print(grid)
		print(value)
		print(node)
		

		data_json= json.dumps(data)
		headers = {'Content-Type': 'application/json'}
		req= requests.post(url,data=data_json, headers=headers)
		print(req.json())
		
		return render(request, 'Controller/config.html', grid)