import sqlite3

connection = sqlite3.connect("Logs.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM Logs;")
results = cursor.fetchall()
cursor.close()
connection.close()
for a in results:
	print(a)