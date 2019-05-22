import requests
import json
import subprocess
import time
import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError
##Alexandre Santos, 80106

#url = 'http://localhost:8000/'

#headers = {'Content-Type': 'application/json'}


def get_hostname():
	hostname = subprocess.check_output(['hostname'])
	if hostname[4] != "" or hostname[4] is not None:
		return chr(hostname[3]) + chr(hostname[4])
	else:
		return chr(hostname[3])


def node_life_cycle():
	

	producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: json.dumps(x).encode('utf-8'))
	#node_id = get_hostname()
	node_id=1
	#data = {'node': str(node_id) }
	data = {str(node_id): 'wake_up'}

	producer.send('switch', value=data)

	#data_json = json.dumps(data)
	#send = requests.post(url + 'nodeup/', data=data_json, headers= headers)
	
	#if send.status_code == 200:
	#	return 'MSG: ' + str(node_id) +' just woke up!!!'
	#except requests.exceptions.Timeout as e:
	#	continue
	#except requests.exceptions.ConnectionError as e:
	#	continue


	while True:
		try:
			#values = subprocess.check_output('sensors | grep -B 3 "ALARM"', shell=True, universal_newlines=True)
			values = subprocess.check_output('sensors', shell=True)
			if values != None or values != "":
				readings = values.decode('utf-8')
				#node_id = get_hostname()
				
				
				current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

				data = { str(node_id) : [current_date, readings.encode('utf-8')]}
				#producer.send('alerts', value=data)
				
				
			data = { str(node_id) : 'alive' }
			producer.send('switch', value=data)
				
				
				#node_id = 13
				
				
				#data_json = json.dumps(data_values)
				
				#send = requests.post(url + 'sensors/' , data=data_json, headers=headers )

		
		except subprocess.CalledProcessError as e:
			##if values return empty string it raises an error
			continue
		except KafkaError as e:
			print(e)
			continue
		#except requests.exceptions.ConnectionError as e:
		#	continue



		time.sleep(90)




node_life_cycle()



