import time, sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

sys.path.insert(0,"../Convert PDF to PNG/")

import test_insert

class MyHandler(PatternMatchingEventHandler):
	patterns = ["*"]

# Print the filename that is added
	def process(self, event):
		file_path = event.src_path
		# file_name = file_path.split("/")[len(file_path.split("/"))-1]
		# test_insert.convert(file_name)
		test_insert.convert(file_path)

	def on_created(self, event):
		self.process(event)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "USAGE: python filename.py ./path/to/folder"
	else:
		args = sys.argv[1:]
		observer = Observer()
		# observer.schedule(MyHandler(), path=args[0] if args else '.')
		observer.schedule(MyHandler(), path=args[0])
		observer.start()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			observer.stop()

		observer.join()