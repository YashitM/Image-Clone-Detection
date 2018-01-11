def convert(filename, file_width, file_height, page_number, pdf_location, file_hash, execution_start_time, log_dictionary, uploaded_file_id, process_start_time, thumbnail_id):
	"""
		This function converts a single Page PDF into a high resolution image and adds the details into the 'image' table
		Input: A Single Page PDF/Image
		Output: A High Resolution Image
	"""

	from wand.image import Image
	from wand.color import Color
	import os
	from database import login_info
	import mysql.connector
	import config
	from PIL import Image as pilImage
	import convert_to_tiles
	import time

	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()
	png_blob = "NULL"
	pdf_blob = "NULL"
	if not os.path.exists(config.store_high_res_images):
		os.makedirs(config.store_high_res_images)
	with Image(filename=filename, resolution=config.high_res_value) as img:
		with Image(width=img.width, height=img.height, background=Color("white")) as bg:
			bg.composite(img,0,0)
			bg.save(filename=config.store_high_res_images + filename.replace(config.store_split_pdfs,"") +".png")
	
	im = pilImage.open(config.store_high_res_images + filename.replace(config.store_split_pdfs,"") +".png")
	img_width, img_height = im.size

	page_size = str(file_width) + "," + str(file_height)


	if config.add_high_res_png_into_db == 1:
		with open(config.store_high_res_images + filename.replace(config.store_split_pdfs,"") +".png","rb") as img:
			png_blob = img.read()

	if config.add_split_pdf_into_database == 1:
		with open(pdf_location, "rb") as pdf:
			pdf_blob=pdf.read()

	# sql_query = """INSERT INTO `image` (`id`, `album_id`, `user_id`, `upload_file_id`, `thumbnail_id`,`page_size`, `png`, `pdf`, `width`, `height`, `page_number`) VALUES (NULL, NULL, NULL, '""" + upload_file_id + """', '""" + str(thumbnail_id) + """', '""" + page_size + """', '""" + png_blob + """' , '""" + pdf_blob + """', '""" + str(img_width) + """', '""" + str(img_height) + """', '""" + str(page_number) + """');"""
	cursor.execute("INSERT INTO `image`(upload_file_id, thumbnail_id, page_size, png, pdf, width, height, page_number) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);", (uploaded_file_id,str(thumbnail_id),page_size,png_blob,pdf_blob,img_width,img_height,""))
	db.commit()
	cursor.close()
	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()
	sql_query = """SELECT * FROM `image` WHERE upload_file_id LIKE '%s' AND page_number LIKE '%s'""" %(uploaded_file_id, str(page_number))
	cursor.execute(sql_query)
	current_image_id = 0
	for row in cursor:
		current_image_id = row[0]
		break
	cursor.close()
	process_end_time = time.time()

	total_time = str(round(process_end_time - process_start_time,config.time_digit_precision))
	print("[" + str(uploaded_file_id) + "," + str(page_number) + "] High Resolution PNG Generated. Details Added to 'image' table. Time: " + total_time)
	config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "," + str(page_number) + "] High Resolution PNG Generated. Details Added to 'image' table. Time: " + total_time)
	log_dictionary['all_steps'] += "[" + str(page_number) + "] High Resolution PNG Generated Details Added to 'image' table. Time: " + total_time + "\n"
	log_dictionary = convert_to_tiles.generate_tiles(config.store_high_res_images + filename.replace(config.store_split_pdfs,"") +".png", current_image_id, log_dictionary, page_number, uploaded_file_id, time.time())
	return log_dictionary
	
if __name__ == '__main__':
	convert("splitPDFs/BlankSmall.pdf0.pdf")
