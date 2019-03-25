from django.shortcuts import render
from rest_framework import viewsets
import json
import requests


# Create your views here.
def home(request):
	return render(request,'Controller/home.html')

def send_shit(request):
		#url = '192.1.1.1/connection'
		url = "http://httpbin.org/post"
		#data = {"SSID":"foo","Frequency":"1234","WEP":"1234123asdgwer"}
		data = {"data":"123"}
		data_json= json.dumps(data)
		headers = {'Content-Type': 'application/json'}
		req= requests.post(url,data=data_json, headers=headers)
		print(req.json())

		return render(request, 'Controller/config.html')