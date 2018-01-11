def handle_image(file_name, uploaded_file_id, file_hash):
	"""
		This function handles the uploaded files that are detected as images.
		Input: Uploaded Image file
		Output: 
	"""
	import magic
	from PIL import Image
	import os
	import json
	import mysql.connector
	from database import login_info
	import config
	import shutil
	import compareCompatibleFiles
	import convert_to_tiles
	import time
	execution_start_time = time.time()
	log_dictionary = {}
	log_dictionary['all_steps'] = "Image Detected\n"
	file_type = magic.from_file(file_name, mime=True)
	if "png" not in file_type:
		conversion_start_time = time.time()
		if not os.path.exists(config.store_converted_images):
			os.makedirs(config.store_converted_images)
		im = Image.open(file_name)
		new_filename = file_name.replace(config.store_main_uploads,config.store_converted_images)
		new_filename = new_filename.split(".")[0] + ".png"
		im.save(new_filename)
		file_name = new_filename
		conversion_end_time = time.time()
		total_time = str(round(conversion_end_time - conversion_start_time,config.time_digit_precision))

		print("[" + str(uploaded_file_id) + "] Converting Image to PNG. Time: " + total_time)
		log_dictionary['all_steps'] += "Converting Image to PNG. Time: %s\n" %(total_time)
		config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] Converting Image to PNG. Time: " + total_time)


	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	img_info = {}	

	image = Image.open(file_name)
	source_width, source_height = image.size

	img_info['dimensions'] = {"width": str(source_width), "height": str(source_height)}
	sql_query = 'UPDATE upload_file SET doc_info = "' + (str(json.dumps(img_info)).replace('"','\\"')).replace("'","\\'") + '", processed="1" WHERE processed="0" AND hash LIKE "' + file_hash + '";'
	cursor.execute(sql_query)
	db.commit()
	cursor.close()
	print("[" + str(uploaded_file_id) + "] Added Image details to 'upload_file' table")
	log_dictionary['all_steps'] += "Added Image details to 'upload_file' table\n"
	config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] Added Image details to 'upload_file' table")

	thumbnail_generation_start_time = time.time()
	newHeight = float(config.fixed_thumbnail_height)
	factor = newHeight/source_height
	newWidth = source_width*factor
	image.thumbnail((newWidth,newHeight), Image.ANTIALIAS)
	if not os.path.exists(config.store_thumbnails):
		os.makedirs(config.store_thumbnails)
	if config.store_converted_images in file_name:
		newfile_location = config.store_thumbnails+file_name.replace(config.store_converted_images,"")+".png"
	else:
		newfile_location = config.store_thumbnails+file_name.replace(config.store_main_uploads,"")+".png"
	image.save(newfile_location)

	thumbnail_blob = "NULL"
	generatedBy = "PNG"
	orientation = ""

	if config.add_thumb_blob_into_db == 1:
		with open(newfile_location,"rb") as img:
			thumbnail_blob = img.read()

	if source_width > source_height:
		orientation = "Landscape"
	else:
		orientation = "Portrait"

	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()
	cursor.execute("INSERT INTO `thumbnail` VALUES (NULL, %s, %s, %s, %s, %s, %s)",(newfile_location,str(source_width),str(source_height),orientation,generatedBy,thumbnail_blob,))
	db.commit()
	cursor.close()
	thumbnail_generation_end_time = time.time()
	total_time = str(round(thumbnail_generation_end_time - thumbnail_generation_start_time,config.time_digit_precision))
	print("[" + str(uploaded_file_id) + "] Thumbnail Generation Complete. Added Details to 'thumbnail' table. Time: " + total_time)
	log_dictionary['all_steps'] += "Thumbnail Generation Complete. Added Details to 'thumbnail' table. Time: " + total_time +"\n"
	config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] Thumbnail Generation Complete. Added Details to 'thumbnail' table. Time: " + total_time)

	comparison_start_time = time.time()
	checkVariable, similarThumbnailID = compareCompatibleFiles.compare(newfile_location, uploaded_file_id, "NULL", source_width, source_height)
	comparison_end_time = time.time()
	total_time = str(round(comparison_end_time - comparison_start_time,config.time_digit_precision))
	print("[" + str(uploaded_file_id) + '] Thumbnails Compared. Comparison Details added to \'thumb_comparison\' table. Time: ' + total_time)
	log_dictionary['all_steps'] += 'Thumbnails Compared. Comparison Details added to \'thumb_comparison\' table. Time: ' + total_time + "\n"
	config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + '] Thumbnails Compared. Comparison Details added to \'thumb_comparison\' table. Time: ' + total_time)

	if checkVariable == "True":
		high_res_start_time = time.time()
		png_blob = ""
		if config.store_converted_images in file_name:
			shutil.copy(file_name, file_name.replace(config.store_converted_images, config.store_high_res_images))
		else:
			shutil.copy(file_name, file_name.replace(config.store_main_uploads, config.store_high_res_images))
		if config.add_high_res_png_into_db == 1:
			with open(file_name,"rb") as img:
				png_blob = img.read()
			# print("[" + str(uploaded_file_id) + "," + str(page_number) + "] High Resolution PNG Generated. Details Added to 'image' table. Time: " + total_time)
		db = mysql.connector.Connect(**login_info)
		cursor=db.cursor()
		sql_query = "SELECT * FROM `thumbnail` WHERE dir LIKE '" + newfile_location + "'"	
		cursor.execute(sql_query)
		thumbnail_id = 0
		for row in cursor:
			thumbnail_id = row[0]
			break
		cursor.close()
		
		db = mysql.connector.Connect(**login_info)
		cursor=db.cursor()
		cursor.execute("INSERT INTO `image` VALUES (NULL, NULL, NULL, %s, %s, %s, %s, %s, %s, %s, %s);", (uploaded_file_id,str(thumbnail_id),"NULL",png_blob,"NULL",str(source_width),str(source_height),"",))
		db.commit()
		high_res_end_time = time.time()
		total_time = str(round(high_res_end_time - high_res_start_time,config.time_digit_precision))
		print("[" + str(uploaded_file_id) + "] High Resolution PNG Generated. Details Added to 'image' table. Time: " + total_time)
		log_dictionary['all_steps'] += "High Resolution PNG Generated. Details Added to 'image' table. Time: " + total_time + "\n"
		config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] High Resolution PNG Generated. Details Added to 'image' table. Time: " + total_time)

		db = mysql.connector.Connect(**login_info)
		cursor=db.cursor()
		sql_query = """SELECT * FROM `image` WHERE upload_file_id LIKE '%s' AND page_number LIKE '%s'""" %(uploaded_file_id, "")
		cursor.execute(sql_query)
		current_image_id = 0
		for row in cursor:
			current_image_id = row[0]
			break
		cursor.close()
		tiles_start_time = time.time()
		log_dictionary = convert_to_tiles.generate_tiles(file_name, current_image_id, log_dictionary, "NULL", uploaded_file_id, tiles_start_time)
	else:
		# print("[" + str(uploaded_file_id) + '] Thumbnails Compared. Comparison Details added to \'thumb_comparison\' table.')
		log_dictionary['all_steps'] += 'Thumbnail matches with Thumbnail ID: ' + similarThumbnailID + '\n'
		# Dont convert, abort process
	if config.keep_converted_images == 0 and config.store_converted_images in file_name:
		os.remove(file_name)
	log_dictionary['total_time'] = str(time.time() - execution_start_time)
	sql_query = "UPDATE upload_file SET log = '" + (str(json.dumps(log_dictionary)).replace('"','\\"')).replace("'","\\'") + "' WHERE hash = '" + file_hash + "' AND processed = '1'"
	db = mysql.connector.Connect(**login_info)
	cursor = db.cursor()
	cursor.execute(sql_query)
	db.commit()
	cursor.close()





		