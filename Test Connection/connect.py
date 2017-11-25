import mysql.connector

try:
	conn = mysql.connector.connect(host='mssql6.gear.host',
								   database='testtable',
								   user='testtable',
								   password='Ob8wia?~Z8Fh')
	if conn.is_connected():
		print('Connected to MySQL database')

except Error as e:
	print(e)
