from django.shortcuts import render

import json
import requests

grid={'1':('OFF','red'),'2':('OFF','red'),'3':('OFF','red'),'4':('OFF','red'),'5':('OFF','red'),'6':('OFF','red'),'7':('OFF','red'),'8':('OFF','red'),'9':('OFF','red'),'10':('OFF','red'),'11':('OFF','red'),'12':('OFF','red'),'13':('OFF','red'),'14':('OFF','red'),'15':('OFF','red'),'16':('OFF','red'),'17':('OFF','red'),'18':('OFF','red'),'19':('OFF','red'),'20':('OFF','red'),'21':('OFF','red'),'22':('OFF','red'),'23':('OFF','red'),'24':('OFF','red')}
# Create your views here.
def home(request):
	return render(request,'Controller/home.html')

def send_grid(request):
	node_grid = grid
	return render(request,'Controller/config.html',{'node_grid':node_grid})

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
			grid[node] =('ON',"green")
		else:
		#turn off
			print("blablablabla")
			grid[node] =('OFF',"red")
		#
		print(grid['1'])
		print(grid)
		print(value)
		print(node)
		
		node_grid = grid
		data_json= json.dumps(data)
		headers = {'Content-Type': 'application/json'}
		req= requests.post(url,data=data_json, headers=headers)
		print(req.json())
		
		return render(request, 'Controller/config.html',{'node_grid':node_grid})