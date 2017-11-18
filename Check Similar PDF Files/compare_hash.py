def compare(file_hash):
	"""
	This function connects to the database and compares the current file's Hash to already existing files.
	If it finds a file with the same hash it will delete it.
	"""
	import mysql.connector
	from database import login_info
	import os

	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	cursor.execute('SELECT pdf_id, file_dir, hash FROM tbl_uploads WHERE processed LIKE "TRUE"')

	for (pdf_id, file_path, existing_hash) in cursor:
		if existing_hash == file_hash:
			cursor.execute('DELETE FROM tbl_uploads WHERE hash LIKE ' + file_hash + ' AND processed LIKE "FALSE"')
			os.remove(file_path)
			# assuming uploads folder is in the same directory as the script

	cursor.close()