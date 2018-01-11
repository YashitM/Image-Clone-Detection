def compute_hash(file_name):
	"""
	Returns the sha256 hash of the bytes of the file given as argument.
	"""
	import hashlib
	BUF_SIZE = 65536
	sha256 = hashlib.sha256()

	with open(file_name, 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			sha256.update(data)
	return sha256.hexdigest()

def split_pdfs(file_name, execution_start_time, uploaded_file_id):
	"""
    This scipt will convert single pdf file with multiple pages into individual PDF files. Then carry out the rest of the functionality: Convert to thumnbail, compare generated thumbnail, generate high resolution image and also generate tiles.
    Input: Uploaded PDF
    Output: Individual Page PDFs
    """

	from PyPDF2 import PdfFileWriter, PdfFileReader
	import time
	import convert_single_file
	import config
	import os
	from database import login_info
	import convert_to_high_res_png
	import mysql.connector
	import compareCompatibleFiles
	import json

	log_dictionary = {}	

	file_hash = compute_hash(file_name)
	start = time.time()
	inputpdf = PdfFileReader(open(file_name, "rb"))

	log_dictionary['all_steps'] = "Splitting PDF File into " + str(inputpdf.numPages) + " Pages\n"

	print("[" + str(uploaded_file_id) + "] Splitting PDF File into " + str(inputpdf.numPages) + " Pages")
	config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] Splitting PDF File into " + str(inputpdf.numPages) + " Pages")
	for i in xrange(inputpdf.numPages):
		output = PdfFileWriter()
		output.addPage(inputpdf.getPage(i))
		if not os.path.exists(config.store_split_pdfs):
			os.makedirs(config.store_split_pdfs)
		with open(config.store_split_pdfs+file_name.replace(config.store_main_uploads,"")+"%s.pdf" % i, "wb") as outputStream:
		# with open(config.store_split_pdfs+file_name.replace(config.store_main_uploads,"")+"%s.pdf" % i, "wb") as outputStream:
			output.write(outputStream)

		new_file = PdfFileReader(open(config.store_split_pdfs+file_name.replace(config.store_main_uploads,"")+"%s.pdf" % i, 'rb'))
		file_width = new_file.getPage(0).mediaBox.getWidth()
		file_height = new_file.getPage(0).mediaBox.getHeight()

		orientation = ""

		if file_width > file_height:
			orientation = "Landscape"
		else:
			orientation = "Portrait"

		start_thumbnail_generation = time.time()
		image_width, thumbnail_image_name, thumbnail_id = convert_single_file.convert_pdf_to_png(config.store_split_pdfs+file_name.replace(config.store_main_uploads,"")+"%s.pdf" % i, orientation, "PDF", uploaded_file_id, file_width, file_height)
		end_thumbnail_generation = time.time()

		total_time = str(round(end_thumbnail_generation - start_thumbnail_generation,config.time_digit_precision))

		log_dictionary['all_steps'] += '[' + str(i) + '] Thumbnail Generation Complete. Added Details to \'thumbnail\' table. Time: ' + total_time + '\n'
		print("[" + str(uploaded_file_id) + ',' + str(i) + '] Thumbnail Generation Complete. Added Details to \'thumbnail\' table  Time: ' + total_time)
		config.write_to_file(config.log_file_name, "[" + str(uploaded_file_id) + ',' + str(i) + '] Thumbnail Generation Complete. Added Details to \'thumbnail\' table  Time: ' + total_time)
		log_dictionary['all_steps'] += "Finding existing images to compare with\n"

		start_thumbnail_comparison = time.time()
		checkVariable, similarThumbnailID = compareCompatibleFiles.compare(thumbnail_image_name, uploaded_file_id, str(i), file_width, file_height)
		end_thumbnail_comparison = time.time()

		total_time = str(round(end_thumbnail_comparison - start_thumbnail_comparison,config.time_digit_precision))

		log_dictionary['all_steps'] += '[' + str(i) + '] Thumbnails Compared. Comparison Details added to \'thumb_comparison\' table' + total_time + '\n'
		print("[" + str(uploaded_file_id) + ',' + str(i) + '] Thumbnails Compared. Comparison Details added to \'thumb_comparison\' table. Time: ' + total_time)
		config.write_to_file(config.log_file_name, "[" + str(uploaded_file_id) + ',' + str(i) + '] Thumbnails Compared. Comparison Details added to \'thumb_comparison\' table. Time: ' + total_time)
		if checkVariable == "True":
			log_dictionary = convert_to_high_res_png.convert(config.store_split_pdfs+file_name.replace(config.store_main_uploads,"")+"%s.pdf" % i, file_width, file_height, i, file_name, file_hash, execution_start_time, log_dictionary, uploaded_file_id, time.time(), thumbnail_id)
		else:
			log_dictionary['all_steps'] += '[' + str(i) + '] Thumbnail matches with Thumbnail ID: ' + similarThumbnailID + '\n'
			# log_dictionary['page'+str(i)]['time'] = str(time.time() - execution_start_time)

		if config.keep_split_pdf_pages == 0:
			os.remove(config.store_split_pdfs+file_name.replace(config.store_main_uploads,"")+"%s.pdf" % i)
	log_dictionary['total_time'] = str(time.time() - execution_start_time)
	sql_query = "UPDATE upload_file SET log = '" + (str(json.dumps(log_dictionary)).replace('"','\\"')).replace("'","\\'") + "' WHERE hash = '" + file_hash + "' AND processed = '1'"
	db = mysql.connector.Connect(**login_info)
	cursor = db.cursor()
	cursor.execute(sql_query)
	db.commit()
	cursor.close()

if __name__ == '__main__':
	# Enter the file name here
	file_name = "testingSmallA.pdf"
	split_pdfs(file_name)
