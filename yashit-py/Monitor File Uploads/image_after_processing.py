def handle_image(file_name)
	import magic
	from PIL import Image
	import os

	def checkFile(file_name):
		"""
		This function checks if the file types is not Png if not it will change it to PNG image
		and delete the existing file. After that it will connect to database and update
		the file's info with dimensions and xmp_info
		"""
		file_type = magic.from_file(file_name, mime=True)
		if "png" not in file_type:
			changeToPngAndSave(file_name)
			deleteExisting(file_name)

		dimensions = getDimensions(file_name)
			
		import mysql.connector
		from database import login_info
		import os

		db = mysql.connector.Connect(**login_info)
		cursor=db.cursor()

		sql_query = 'UPDATE tbl_uploads SET file_doc_info = "' + dimensions + " " + xmp_info + '", processed="TRUE" WHERE processed="FALSE" AND file_dir LIKE "' + file_name + '";'
		cursor.execute()

		cursor.close()


	def getDimensions(file_name):
		"""
		Returns the dimesnsions of the file as a string.
		"""
		im = Image.open(filePath)
		width, height = im.size
		dimensions = "(" + str(width) + "," + str(height) + ")"
		return dimensions

	def changeToPngAndSave(file_name):
		"""
		Changes other image formats to png and saves it to the disk.
		"""
		im = Image.open(file_name)
		im.save(file_name.split("/")[-1].split(".")[0]+'.png')

	def deleteExisting(file_name):
		"""
		Deletes the file given as argument from the disk.
		"""
		os.remove(file_name)

	checkFile(file_name)