import sqlite3

connection = sqlite3.connect("test.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM test;")
results = cursor.fetchall()
for a in results:
	print(a)