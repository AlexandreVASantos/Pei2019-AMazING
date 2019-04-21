import time
import subprocess
import requests
import daemon

##Alexandre Santos, 80106

url = 'x.x.x.x/get_readings'

headers = {'Content-Type': 'application/json'}

def get_readings():
	
	while True:
		try:
			values = subprocess.check_output(['sensors','| grep "ALARM"'])

			data_values = {'data', values}

			data_json = json.dumps(data_values)
			requests.post(url, data=data_json, headers=headers )
		
		except requests.exceptions.HTTPError as e:
			return str(e)



		time.sleep(3600)


get_readings()