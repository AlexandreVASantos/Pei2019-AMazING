import requests
import json
import subprocess
import datetime
import time

##Alexandre Santos, 80106

url = 'http://192.168.1.74:8000/'

headers = {'Content-Type': 'application/json'}


def get_hostname():
	hostname = subprocess.check_output(['hostname'])
	if hostname[4] != "" or hostname[4] is not None:
		return chr(hostname[3]) + chr(hostname[4])
	else:
		return chr(hostname[3])

def wake_up():

	try:
		node_id = get_hostname()
		data = {'node': str(node_id) }

		data_json = json.dumps(data)
		send = requests.post(url + 'nodeup/', data=data_json, headers= headers)
	except requests.exceptions.HTTPError as e:
		return str(e)

	return 'MSG: ' + str(node_id) +' just woke up!!!'


def get_readings():
	
	while True:
		try:
			values = subprocess.check_output('sensors | grep -B 3 "ALARM"', shell=True, universal_newlines=True)

			if values != None or values != "":
				readings = values.decode('utf-8')
				todays_date = datetime.datetime.now()

				node_id = get_hostname()
				data_values = {'node' : node_id ,'readings' : str(readings), 'date' : todays_date.strftime("%Y-%m-%d")}
				
				data_json = json.dumps(data_values)
				
				requests.post(url + 'sensors/' , data=data_json, headers=headers )
		
		except requests.exceptions.HTTPError as e:
			return str(e)
		except subprocess.CalledProcessError as e:
			##if values return empty string it raises an error
			continue



		time.sleep(900)




node = wake_up()
print(node)
readings = get_readings()
