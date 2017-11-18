def handle_image(file_name)
	import magic
	from PIL import Image
	import os

	def checkFile(file_name):
		file_type = magic.from_file(file_name, mime=True)
		if "png" in file_type:
			changeToPngAndSave(file_name)
			deleteExisting(file_name)

	def changeToPngAndSave(file_name):
		im = Image.open(file_name)
		im.save(file_name.split("/")[-1].split(".")[0]+'.png')

	def deleteExisting(file_name):
		os.remove(file_name)

	checkFile(file_name)