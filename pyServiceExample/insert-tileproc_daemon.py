#!/usr/bin/python

import signal
import time
import sys
import multiprocessing as mp
import insert_daemon as sp1
import tile_proc_daemon as sp2

# Processes
scripts = [ \
	mp.Process(target=sp1.main), \
	mp.Process(target=sp2.main) \
]

def log_files():
	# sys.stdout = open("log.txt", 'w', buffering=0)
	# sys.stderr = open("err.txt", 'w', buffering=0)
	pass

class ElegantExit(Exception):
	pass

def signal_handler(signum, frame):
	print "Recibido!", signum
	raise ElegantExit()

def trap_signals():
	signal.signal(signal.SIGTERM, signal_handler)

def stop_scripts():
	try:
		for p in scripts:
			p.terminate()
			p.join()
		print "Finished!"
	except BaseException as e:
		print e
		print "Something happened!"

def start_scripts():
	for p in scripts:
		p.start()

def keep_waiting():
	s = 0
	while True:
		time.sleep(1)
		s += 1
	return s

def main():
	secs = 0
	log_files()
	try:
		trap_signals()
		start_scripts()	
		secs = keep_waiting()
	except BaseException as e:
		print "Script alive for:", secs
		print e
		stop_scripts()

if __name__ == "__main__":
	main()

