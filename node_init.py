import requests
import json
import subprocess
import time


##Alexandre Santos, 80106

url_wake = 'x.x.x.x/node_up'
url_readings = 'x.x.x.x/get_readings'
headers = {'Content-Type': 'application/json'}


def get_hostname():
	hostname = subprocess.check_output(['hostname'])
	return hostname[3]

def wake_up():

	try:
		node_id = get_hostname()
		data = {'node': node_id }
		data_json = json.dumps(data)
		send = requests.post(url, data=data_json, headers= headers)
	except requests.exceptions.HTTPError as e:
		return str(e)

	return 'MSG: ' + str(node_id) +' just woke up!!!'


def get_readings():
	
	while True:
		try:
			values = subprocess.check_output(['sensors','| grep "ALARM"'])
			node_id = get_hostname()
			data_values = {"node" : node_id ,' data' : values}

			data_json = json.dumps(data_values)
			requests.post(url, data=data_json, headers=headers )
		
		except requests.exceptions.HTTPError as e:
			return str(e)



		time.sleep(3600)




node = wake_up()
readings = get_readings()