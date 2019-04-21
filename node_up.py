import requests
import json
import subprocess


##Alexandre Santos, 80106

url = 'x.x.x.x/node_up'
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



value = wake_up()