# To run, python compare_hash.py

def compare(file_hash):
	"""
    This script will check the hash of the newly entered file with the existing hashes in the database. 
    """
	import mysql.connector
	from database import login_info
	import os

	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	cursor.execute('SELECT pdf_id, file_dir, hash FROM tbl_uploads_test WHERE processed LIKE "TRUE"')

	for (pdf_id, file_path, existing_hash) in cursor:
		if existing_hash == file_hash:
			cursor.execute('DELETE FROM tbl_uploads_test WHERE hash LIKE ' + file_hash + ' AND processed LIKE "FALSE"')
			os.remove(file_path)
			print("File already exists! Removing it")
			# assuming uploads folder is in the same directory as the script

	cursor.close()

if __name__ == '__main__':
	# Enter a test hash to check whether the script works
	file_hash = ""
	compare(file_hash)