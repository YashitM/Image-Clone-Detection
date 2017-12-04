def find_similar_thumbnails(filename):
	import os
	directory_name = "uploads/"
	all_files = os.listdir(directory_name)
	for i in all_files:
		os.system("node compare.js " + i)

if __name__ == '__main__':
	find_similar_thumbnails("lol")