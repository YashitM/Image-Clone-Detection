import time, sys
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# USAGE: python fileanme.py ./foldername

class MyHandler(PatternMatchingEventHandler):
    patterns = ["*"]

# Print the filename that is added
    def process(self, event):
        print event.src_path

    def on_created(self, event):
        self.process(event)

if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else '.')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()