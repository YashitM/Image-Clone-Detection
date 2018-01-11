def compare(current_file_hash, file_path, execution_start_time, uploaded_file_id):
	"""
		This script will check the hash of the newly entered file with the existing hashes from the upload_file table.
		If a similar file is found, the process will be stopped for this file. And details will be added to the log of this file in the upload_file table.
		Input: Newly Uploaded file.
		Output: Rejects the file if hash is not unique.
	"""
	import mysql.connector
	from database import login_info
	import os
	import json
	import config
	import time

	print("[" + str(uploaded_file_id) + "] Checking For Existing Copies within 'upload_file' table")
	config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] Checking For Existing Copies within 'upload_file' table")
	log_dictionary = {}
	log_dictionary['all_steps'] = "Checking For Existing Copies within 'upload_file' table"

	db = mysql.connector.Connect(**login_info)
	cursor = db.cursor(buffered=True)

	cursor.execute('SELECT * FROM upload_file WHERE processed LIKE "1"')

	for row in cursor:
		db_file_hash = row[4]
		if db_file_hash == current_file_hash:
			os.remove(file_path)
			db2 = mysql.connector.Connect(**login_info)
			cursor_delete = db2.cursor()
			log_dictionary['all_steps'] += 'Rejected. Hash Matches with File Number: ' + str(row[0]) + '\n'
			total_time = str(round(time.time() - execution_start_time,config.time_digit_precision))
			print("[" + str(uploaded_file_id) + "] Rejected. Hash Matches with File Number: " + str(row[0]) + ". Time: " + total_time)
			config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] Rejected. Hash Matches with File Number: " + str(row[0]) + ". Time: " + total_time)
			log_dictionary['total_time'] = "Time: " + total_time + "\n"
			json_string = json.dumps(log_dictionary)
			cursor_delete.execute('UPDATE upload_file SET log = "' + (str(json_string).replace('"','\\"')).replace("'","\\'") + '", processed = "2" WHERE hash LIKE "' + current_file_hash + '" AND processed LIKE "0"')
			db2.commit()

			cursor_delete.close()
			cursor.close()
			return False

	cursor.close()
	return True


if __name__ == '__main__':
	# Enter a test hash to check whether the script works
	file_hash = ""
	file_path = ""
	compare(file_hash, file_path)
