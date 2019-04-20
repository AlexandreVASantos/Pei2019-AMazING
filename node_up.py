import requests
import json
import subprocess


url = 'x.x.x.x/node_up'


def get_hostname():
	hostname = subprocess.check_output(['hostname'])
	return hostname[3]

def wake_up():
	node_id = get_hostname()
	data = {'node': node_id }
	data_json = json.dumps(data)
	send = requests.post(url, data=data_json, headers= {'Content-Type': 'application/json'})