"""
Obsesrver file which observes a perticular directory for any changes.
If a file is added it prints/returns the file's name.
"""

import time, sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import magic
import pdf_after_processing
import image_after_processing
import threading
import Queue
import compare_hash
import split
import config
import os
import time
import mysql.connector
from database import login_info

def worker1():
	while True:
		item = q1.get()
		item1 = item.split(";;;")[0]
		item2 = item.split(";;;")[1]
		item3 = item.split(";;;")[2]
		split.split_pdfs(item1, float(item2), item3)
		q1.task_done()

def compute_hash(file_name):
	"""
	Returns the sha256 hash of the bytes of the file given as argument.
	"""
	import hashlib
	BUF_SIZE = 65536
	sha256 = hashlib.sha256()

	with open(file_name, 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			sha256.update(data)
	return sha256.hexdigest()


def main_worker(file_path, uploaded_file_id):

	time.sleep(0.5)
	try:
		if uploaded_file_id == 0:
			db = mysql.connector.Connect(**login_info)
			cursor = db.cursor()
			computed_file_hash = compute_hash(file_path)
			sql_query = "SELECT * FROM upload_file WHERE hash LIKE '" + computed_file_hash + "' AND processed LIKE '0' ORDER BY id DESC"
			cursor.execute(sql_query)
			for row in cursor:
				uploaded_file_id = row[0]
				break

		print("[" + str(uploaded_file_id) + "] New File " + file_path + ". Details added to 'upload_file' table")
		config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] New File " + file_path + ". Details added to 'upload_file' table")
		start_time = time.time()
		if compare_hash.compare(computed_file_hash, file_path, start_time, uploaded_file_id):
			print("[" + str(uploaded_file_id) + "] No Matches Found based on SHA-256 hash. Time: " + str(round(time.time() - start_time,config.time_digit_precision)))
			config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] No Matches Found based on SHA-256 hash. Time: " + str(round(time.time() - start_time,config.time_digit_precision)))
			file_type = magic.from_file(file_path, mime=True)
			if ("png" in str(file_type)) or ("jpeg" in str(file_type)) or ("bmp" in str(file_type)):
				# Send it to PNG Function
				print("[" + str(uploaded_file_id) + "] Image Detected")
				config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] Image Detected")
				image_after_processing.handle_image(file_path, uploaded_file_id, computed_file_hash)
			elif "pdf" in file_type:
				# Send it to PDF function
				print("[" + str(uploaded_file_id) + "] PDF Detected")
				config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] PDF Detected")
				pdf_after_processing.handle_pdf(computed_file_hash, file_path, uploaded_file_id)
				q1.put(file_path + ";;;" + str(start_time) + ";;;" + str(uploaded_file_id))

			if config.keep_uploaded_files == 0:
				os.remove(file_path)
	except Exception as e:
		print("Error: " + e)
		config.write_to_file(config.error_file_name, e)

class MyHandler(PatternMatchingEventHandler):
	patterns = ["*"]

	def process(self, event):
		main_worker(event.src_path, 0)

	def on_created(self, event):
		self.process(event)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print ("USAGE: python filename.py /path/to/folder")
	else:
		db = mysql.connector.Connect(**login_info)
		cursor = db.cursor()
		sql_query = "SELECT * FROM upload_file WHERE processed LIKE '0'"
		cursor.execute(sql_query)
		num_not_processed = 0
		for i in cursor:
			num_not_processed += 1
		print("[+] Found " + str(num_not_processed) + " unprocessed files")
		if num_not_processed > 0:
			for row in cursor:
				main_worker(row[9],row[0])
		args = sys.argv[1:]
		observer = Observer()
		q1 = Queue.Queue()
		for i in range(config.number_of_threads):
			t1 = threading.Thread(target=worker1)
			t1.daemon = True
			t1.start()
		observer.schedule(MyHandler(), path=args[0])
		observer.start()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			observer.stop()

		observer.join()
