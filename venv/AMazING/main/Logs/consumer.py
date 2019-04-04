from json import loads
from kafka import KafkaConsumer
import sqlite3
import sys


consumer = KafkaConsumer('numtest', bootstrap_servers=['localhost:9092'], auto_offset_reset='earliest', enable_auto_commit=True, group_id='my_group', value_deserializer=lambda x:loads(x.decode('utf-8')))
count = 0
for message in consumer:
	count = count+1
	connection = sqlite3.connect("test.db")
	cursor = connection.cursor()
	message = message.value
	for (a,b) in message.items():
		print("("+str(a)+"',' "+str(b[0])+"',' "+str(b[1])+"',' "+str(b[2]) + ") values entered")
		cursor.execute("INSERT INTO test VALUES('"+ str(a)+"',' "+str(b[0])+"',' "+str(b[1])+"',' "+str(b[2])+"');")
		connection.commit()
	cursor.close()
	connection.close()