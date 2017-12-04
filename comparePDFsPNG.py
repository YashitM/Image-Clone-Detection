def comparePDFsPNG(fileName):
	import os
	directoryName = "./thumbnails/"
	files = os.listdir(directoryName)
	for i in files:
		print ("node \"Test Folders\Compare Files\compare.js\" \"" + fileName + "\" " + "\"" + directoryName + i + "\"")
		os.system("node \"Test Folders\Compare Files\compare.js\" \"" + fileName + "\" " + "\"" + directoryName + i + "\"")

if __name__ == '__main__':
	comparePDFsPNG("./thumbnails/46335-testImg_scene green A.pdf0.pdf - Copy.png")