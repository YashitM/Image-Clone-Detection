def convert_pdf_to_png(filename, orientation, generatedBy, uploaded_file_id, file_width, file_height):
	"""
		This function converts a single PDF page into a thumbnail whose details are added to the 'thumbnail' table.
		INPUT: Single page PDF file
		OUTPUT: Thumbnail Image
	"""

	import time
	from wand.image import Image
	from wand.color import Color
	from PIL import Image as pilImage
	import os
	import config
	from database import login_info
	import mysql.connector

	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	thumbnail_blob = "NULL"
	with Image(filename=filename, resolution=100) as img:
		with Image(width=img.width, height=img.height, background=Color("white")) as bg:
			bg.composite(img,0,0)
			bg.save(filename=filename+".png")

	image = pilImage.open(filename+".png")
	width, height = image.size
	newHeight = float(config.fixed_thumbnail_height)
	factor = newHeight/height
	newWidth = width*factor
	image.thumbnail((newWidth,newHeight), pilImage.ANTIALIAS)
	if not os.path.exists(config.store_thumbnails):
		os.makedirs(config.store_thumbnails)
	image.save(config.store_thumbnails+filename.replace(config.store_split_pdfs,"")+".png")

	if config.keep_split_pdf_pages == 0:
		os.remove(filename+".png")

	if config.add_thumb_blob_into_db == 1:
		with open(config.store_thumbnails+filename.replace(config.store_split_pdfs,"")+".png","rb") as img:
			thumbnail_blob = img.read()
	
	# sql_query = """INSERT INTO `thumbnail` (`id`, `dir`, `width`, `height`, `orientation`, `generatedBy`, `png`) VALUES (NULL, '""" + config.store_thumbnails+filename.replace(config.store_split_pdfs,"")+".png" + """', '""" + str(newWidth) + """', '""" + str(float(config.fixed_thumbnail_height)) + """', '""" + orientation + """', '""" + generatedBy + """', '""" + thumbnail_blob + """');"""

	new_filename = config.store_thumbnails+filename.replace(config.store_split_pdfs,"")+".png"

	cursor.execute("INSERT INTO `thumbnail` VALUES (NULL, %s, %s, %s, %s, %s, %s)",(new_filename,str(file_width),str(file_height),orientation,generatedBy,thumbnail_blob,))
	db.commit()
	cursor.close()

	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	sql_query = "SELECT * FROM `thumbnail` WHERE dir LIKE '" + config.store_thumbnails+filename.replace(config.store_split_pdfs,"")+".png" + "'"

	cursor.execute(sql_query)
	thumbnail_id = 0
	for row in cursor:
		thumbnail_id = row[0]

	return newWidth, config.store_thumbnails+filename.replace(config.store_split_pdfs,"")+".png", thumbnail_id

if __name__ == '__main__':
	import os
	directory = "basedir/"
	all_files = os.listdir(directory)
	for i in all_files:
		convert_pdf_to_png(directory + i)
