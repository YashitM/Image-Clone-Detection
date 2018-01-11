"""
	This function resets the database by removing all existing data and recreating the table structure
"""

from database import login_info
import mysql.connector
import os
import config

db = mysql.connector.Connect(**login_info)
cursor=db.cursor()

cursor.execute("""DROP TABLE IF EXISTS users""")
cursor.execute("""
	CREATE TABLE users(
		id INTEGER PRIMARY KEY AUTO_INCREMENT,
		email VARCHAR(100),
		pass VARCHAR(100),
		verification_token VARCHAR(100),
		reset_token VARCHAR(100),
		registered_on VARCHAR(100),
		reset_date VARCHAR(100),
		verified BOOLEAN,
		firstname VARCHAR(100),
		lastname VARCHAR(100)
	)
	""")

cursor.execute("""DROP TABLE IF EXISTS album""")
cursor.execute("""
	CREATE TABLE album(
		id INTEGER PRIMARY KEY AUTO_INCREMENT,
		user_id VARCHAR(100),
		name VARCHAR(100)
	)
	""")

cursor.execute("""DROP TABLE IF EXISTS upload_file""")
cursor.execute("""
	CREATE TABLE upload_file(
		id INTEGER PRIMARY KEY AUTO_INCREMENT,
		user_id VARCHAR(100),
		album_id VARCHAR(100),
		timeUploaded VARCHAR(100),
		hash VARCHAR(100),
		type VARCHAR(100),
		size VARCHAR(100),
		doc_info VARCHAR(10000),
		processed VARCHAR(10),
		dir VARCHAR(500),
		log VARCHAR(10000)
	)
	""")

cursor.execute("""DROP TABLE IF EXISTS image""")
cursor.execute("""
	CREATE TABLE image(
		id INTEGER PRIMARY KEY AUTO_INCREMENT,
		album_id VARCHAR(100),
		user_id VARCHAR(100),
		upload_file_id VARCHAR(100),
		thumbnail_id VARCHAR(100),
		page_size VARCHAR(100),
		png LONGBLOB,
		pdf LONGBLOB,
		width INTEGER(11),
		height INTEGER(11),
		page_number VARCHAR(100),
		sequence INTEGER(11)
	)
	""")


cursor.execute("""DROP TABLE IF EXISTS tiles""")
cursor.execute("""
	CREATE TABLE tiles(
		id INTEGER PRIMARY KEY AUTO_INCREMENT,
		image_id INTEGER(11),
		deepzoom_id VARCHAR(10),
		tile LONGBLOB
	)
	""")


cursor.execute("""DROP TABLE IF EXISTS thumb_comparison""")
cursor.execute("""
	CREATE TABLE thumb_comparison(
		new_image_id INTEGER,
		existing_image_id INTEGER,
		comparison LONGBLOB,
		difference_percentage VARCHAR(100)
	)
	""")

cursor.execute("""DROP TABLE IF EXISTS thumbnail""")
cursor.execute("""
	CREATE TABLE thumbnail(
		id INTEGER PRIMARY KEY AUTO_INCREMENT,
		dir VARCHAR(1000),
		width VARCHAR(100),
		height VARCHAR(100),
		orientation VARCHAR(100),
		generatedBy VARCHAR(100),
		png LONGBLOB
	)
	""")

if config.reset_folders_in_creating_table == 0: #if set to 1, then clears the files and chgrp www-data persmissions
	import shutil

	if os.path.exists(config.store_main_uploads):
		shutil.rmtree(config.store_main_uploads)
	
	if os.path.exists(config.store_split_pdfs):
		shutil.rmtree(config.store_split_pdfs)

	if os.path.exists(config.store_thumbnails):
		shutil.rmtree(config.store_thumbnails)

	if os.path.exists(config.store_high_res_images):
		shutil.rmtree(config.store_high_res_images)

	if os.path.exists(config.store_comparison_images):
		shutil.rmtree(config.store_comparison_images)

	if os.path.exists(config.store_converted_images):
		shutil.rmtree(config.store_converted_images)


	if not os.path.exists(config.store_main_uploads):
		os.makedirs(config.store_main_uploads)
	
	if not os.path.exists(config.store_split_pdfs):
		os.makedirs(config.store_split_pdfs)

	if not os.path.exists(config.store_thumbnails):
		os.makedirs(config.store_thumbnails)

	if not os.path.exists(config.store_high_res_images):
		os.makedirs(config.store_high_res_images)

	if not os.path.exists(config.store_comparison_images):
		os.makedirs(config.store_comparison_images)

	if not os.path.exists(config.store_converted_images):
		os.makedirs(config.store_converted_images)
