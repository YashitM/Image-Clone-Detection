def generate_tiles(filename, image_id, log_dictionary, page_number,uploaded_file_id, process_start_time):
	"""
		This function generates tiles for the high resolution image that is created. The tile details are stored in the 'tiles' table.
		Input: High resolution PNG
		Output: Tiles for the input PNG
	"""

	import tempfile,shutil
	import deepzoom
	import mysql.connector
	from database import login_info
	import config
	import os
	import time

	tmpdir = tempfile.mkdtemp()
	tmpimg=str(image_id)+"_image.png"
	tmpdzi=str(image_id)+"_tmp.dzi"
	image_name = tmpdir+"/"+tmpimg
	dzi_name = tmpdir+"/"+tmpdzi

	with open(image_name, "wb") as img_file:
		with open(filename, "rb") as read_file:
			img_file.write(read_file.read())

	creator = deepzoom.ImageCreator(tile_size=config.tile_pixel_size, tile_overlap=2, tile_format="png",image_quality=1, resize_filter="bicubic")
	creator.create(image_name, dzi_name)
	width, height = creator.image.size

	basepath = tmpdir+"/"+str(image_id)+"_tmp_files"

	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	for d in os.listdir(basepath):
		curpath = os.path.join(basepath,d)
		if os.path.isdir(curpath):
			for f in os.listdir(curpath):
				if os.path.isfile(os.path.join(curpath,f)):
					with open(os.path.join(curpath,f), "rb") as tile_file:
						tile_blob = tile_file.read()
						cursor.execute("INSERT INTO tiles values (NULL,%s,%s,%s)",(str(image_id), d+'_'+f[:-4], tile_blob,))
						db.commit()
	shutil.rmtree(tmpdir)
	cursor.close()
	db.close()

	process_end_time = time.time()
	total_time = str(round(process_end_time - process_start_time,config.time_digit_precision))
	log_dictionary['all_steps'] +="["+ str(page_number) +"] Tile Generation Complete. Details Added to 'tiles' table. Time "+ total_time + "\n"
	print("[" + str(uploaded_file_id) + "," + str(page_number) +"] Generated Tiles and Added Details to 'tiles' table. Time: " + total_time)
	config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "," + str(page_number) +"] Generated Tiles and Added Details to 'tiles' table. Time: " + total_time)
	return log_dictionary

if __name__ == '__main__':
	filename = "highResImages/BlankSmall.pdf0.pdf.png"
	generate_tiles(filename,1)

