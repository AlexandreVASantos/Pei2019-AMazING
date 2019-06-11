import requests
import json
import subprocess
import time
import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError

##Alexandre Santos, 80106

url = 'http://localhost:8000/'

headers = {'Content-Type': 'application/json'}


def get_hostname():
	hostname = subprocess.check_output(['hostname'], shell=True, universal_newlines=True)
	if hostname[4] != "\n" :
		return hostname[3] + hostname[4]
	else:
		return hostname[3]


def node_life_cycle():
	
	time.sleep(60)
	
	while True:
		try:
			
			producer = KafkaProducer(bootstrap_servers=['192.168.85.228:9093'],value_serializer=lambda x: json.dumps(x).encode('utf-8'))
			node_id = str(get_hostname())
			node_id.replace('\n', '')
			data = {node_id: 'wake_up'}
			print(data)

			producer.send('switch', value=data)
			
			producer.close()

			#data_json = json.dumps(data)
			#send = requests.post(url + 'nodeup/', data=data_json, headers= headers)
			break;

		except KafkaError as e:
			print(e)
			continue 	


	while True:
		try:
			producer = KafkaProducer(bootstrap_servers=['192.168.85.228:9093'],value_serializer=lambda x: json.dumps(x).encode('utf-8'))

			data = { node_id : 'alive' }
			print(data)
			producer.send('switch', value=data)
		
			
			
			values = subprocess.check_output('sensors | grep -B 3 "ALARM"', shell=True, universal_newlines=True)
			#values = subprocess.check_output('sensors', shell=True)
			if values != None or values != "":
				readings = values.decode('utf-8')
				node_id = get_hostname()
				
				
				current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

				data = { str(node_id) : [current_date, readings.encode('utf-8')]}
				producer.send('alerts', value=data)
				
				
			
			
			
				
		
		except subprocess.CalledProcessError as e:
			##if values return empty string it raises an error
			pass
		except KafkaError as e:
			print(e)
			continue


		producer.close()
		time.sleep(50)




node_life_cycle()



