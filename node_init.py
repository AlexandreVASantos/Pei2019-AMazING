import requests
import json
import subprocess
import time


##Alexandre Santos, 80106

url_wake = 'http://127.0.0.1:8000/nodeup/'
url_readings = '127.0.0.1:8000/get_readings'
headers = {'Content-Type': 'application/json'}


def get_hostname():
	hostname = subprocess.check_output(['hostname'])
	return hostname[3]

def wake_up():

	try:
		node_id = get_hostname()
		data = {'node': str(node_id) }

		data_json = json.dumps(data)
		send = requests.post(url_wake, data=data_json, headers= headers)
	except requests.exceptions.HTTPError as e:
		return str(e)

	return 'MSG: ' + str(node_id) +' just woke up!!!'


#def get_readings():
#	
#	while True:
#		try:
#			values = subprocess.check_output(['sensors','| grep "ALARM"'])
#			if values != None or values != "":
#				todays_date = datetime.datetime.now()
#
#				node_id = get_hostname()
#				data_values = {'node' : node_id ,' data' : values, 'date' : x.strftime("%Y-%m-%d")}
#
#				data_json = json.dumps(data_values)
#				requests.post(url, data=data_json, headers=headers )
#		
#		except requests.exceptions.HTTPError as e:
#			return str(e)
#
#
#
#		time.sleep(3600)




node = wake_up()
print(node)
#readings = get_readings()
