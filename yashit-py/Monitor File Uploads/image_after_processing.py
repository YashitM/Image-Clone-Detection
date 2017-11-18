def handle_image(file_name)
	import magic
	from PIL import Image
	import os

	def checkFile(file_name):
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
		im = Image.open(filePath)
		width, height = im.size
		dimensions = "(" + str(width) + "," + str(height) + ")"
		return dimensions

	def changeToPngAndSave(file_name):
		im = Image.open(file_name)
		im.save(file_name.split("/")[-1].split(".")[0]+'.png')

	def deleteExisting(file_name):
		os.remove(file_name)

	checkFile(file_name)