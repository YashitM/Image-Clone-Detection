import time, sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import magic
import pdf_after_processing
import image_after_processing
import threading
import Queue

sys.path.insert(0,"../Check Similar PDF Files/")

import compare_hash
import split

def worker():
	while True:
		item = q.get()
		split.split_pdfs(item)
		q.task_done()

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


"""
Below is an obsesrver which observes a perticular directory for any changes.
If a file is added, deleted or renamed it prints/returns the file's name.
"""
class MyHandler(PatternMatchingEventHandler):
	patterns = ["*"]

# Get the file that is added
	def process(self, event):
		file_path = event.src_path
		# Added time delay to guarentee that the database has been filled with the data 
		# Need to check if this is needed on the server
		time.sleep(1)
		# compare_hash.compare(compute_hash(file_path))

		file_type = magic.from_file(file_path, mime=True)
		print(file_type)
		if ("png" in str(file_type)) or ("jpeg" in str(file_type)) or ("bmp" in str(file_type)):
			# Send it to PNG Function
			print("image")
			image_after_processing.handle_image(file_path)
		elif "pdf" in file_type:
			print("PDf")
			# Send it to PDF function
			pdf_after_processing.handle_pdf(file_path)
			# Then send it to the split pdf function
			# split.split_pdfs(file_path)
			q.put(file_path)
	def on_created(self, event):
		self.process(event)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print ("USAGE: python filename.py ./path/to/folder")
	else:
		args = sys.argv[1:]
		observer = Observer()
		q = Queue.Queue()
		for i in range(2):
			t = threading.Thread(target=worker)
			t.daemon = True
			t.start()
		# observer.schedule(MyHandler(), path=args[0] if args else '.')
		observer.schedule(MyHandler(), path=args[0])
		observer.start()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			observer.stop()

		observer.join()