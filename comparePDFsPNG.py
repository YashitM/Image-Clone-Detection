def comparePDFsPNG(fileName):
	import os
	directoryName = config.store_thumbnails
	files = os.listdir(directoryName)
	for i in files:
		print ("node \"Test Folders\Compare Files\compare.js\" \"" + fileName + "\" " + "\"" + directoryName + i + "\"")
		os.system("node \"Test Folders\Compare Files\compare.js\" \"" + fileName + "\" " + "\"" + directoryName + i + "\"")

def compareSameSize(fileName, width, height):
	from database import login_info
	import mysql.connector
	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	cursor.execute("""
		SELECT file_dir FROM tlb_uploads_test WHERE height LIKE %s AND width LIKE %s
		""", width, height)

	for directoryName in cursor:
		os.system("node \"Test Folders\Compare Files\compare.js\" \"" + fileName + "\" " + "\"" + directoryName + i + "\"")

def compareSameOrientation(fileName, orientation):
	from database import login_info
	import mysql.connector
	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	cursor.execute("""
		SELECT orientation FROM tlb_uploads_test WHERE orientation LIKE %s
		""", orientation)

	for directoryName in cursor:
		os.system("node \"Test Folders\Compare Files\compare.js\" \"" + fileName + "\" " + "\"" + directoryName + i + "\"")
		

if __name__ == '__main__':
	comparePDFsPNG("./thumbnails/46335-testImg_scene green A.pdf0.pdf - Copy.png")