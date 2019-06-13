from time import sleep
from json import dumps
from kafka import KafkaProducer
import datetime

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))

for e in range(1000):
    date = datetime.datetime.today().strftime('%B %d, %Y - %H:%M:%S')
    data = {'username' : [date,'Function ID: '+str(e),'input', 'output']}
    producer.send('numtest', value=data)
    sleep(5)