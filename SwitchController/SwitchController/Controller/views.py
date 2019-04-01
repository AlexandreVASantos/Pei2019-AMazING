from django.shortcuts import render

import json
import requests
import os
import subprocess
import sqlite3




grid = {}

# Create your views here.
def home(request):
	return render(request,'Controller/home.html')

def send_grid(request):
	refresh_grid()
	node_grid = grid
	return render(request,'Controller/config.html',{'node_grid':node_grid})

def refresh_grid():
	connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/grid.db")
	c=connection.cursor()
	c.execute("Select * from node;")
	fetch= c.fetchall()
	for row in fetch:
		grid[row[0]] = (row[1],row[2],row[3])
	connection.close()
	


def send_shit(request):
	#os.system('ping google.com')
	subprocess.check_call(['echo','SWITCH ARUBA'])
	#url = 'http://192.1.1.1/connection'
	url = "http://httpbin.org/post"
	#data = {"SSID":"foo","Frequency":"1234","WEP":"1234123asdgwer"}
	data = {"data":"123"}
	dic=request.GET
	for key in dic:
		node=key
		value=dic[key]

	comands = 'telnet x.x.x.x configure terminal interface' 
	
	connection = sqlite3.connect("/home/alexandre/Desktop/SwitchController/SwitchController/Controller/grid.db")
	c=connection.cursor()
	
	if value == 'OFF':
	#turn on
		query = "Update node Set value='ON', color='green' where id="+ node +";"
	else:
	#turn off
		query = "Update node Set value='OFF', color='red' where id=" + node +";"
	
	c.execute(query)
	connection.commit()
	connection.close()
	#
	
	refresh_grid()
	print(grid)
	node_grid = grid
	data_json= json.dumps(data)
	headers = {'Content-Type': 'application/json'}
	req= requests.post(url,data=data_json, headers=headers)
	print(req.json())
	
	return render(request, 'Controller/config.html',{'node_grid':node_grid})