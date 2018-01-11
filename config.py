"""
	1 = True, 0 = False
"""
keep_uploaded_files = 1 
keep_split_pdf_pages = 1
keep_comparison_image = 1
keep_converted_images = 1

add_split_pdf_into_database = 1
add_thumb_blob_into_db = 1
add_comparison_blob_into_db = 1
add_high_res_png_into_db = 1
"""
	Directory Names
"""
store_main_uploads = "uploads/"
store_split_pdfs = "splitPDFs/"
store_thumbnails = "thumbnails/"
store_high_res_images = "highResImages/"
store_comparison_images = "comparisons/"
store_converted_images = "convertedImages/" #Store the images that are converted to PNG from some other image format

"""
	Other
"""
high_res_value = 300
fixed_thumbnail_height = 500
number_of_threads = 10
tile_pixel_size = 250
time_digit_precision = 5
log_file_name = "log.txt"
error_file_name = "err.txt"
reset_folders_in_creating_table = 0

"""
	Common Functions
"""

def write_to_file(filename, text_to_write):
	import os.path
	if not os.path.isfile(filename):
		open(filename,"wt")
	import time
	timestamp = time.strftime("%c")
	f = open(filename,"a")
	f.write(timestamp)
	f.write("\n")
	f.write(text_to_write)
	f.write("\n")
	f.close()


"""
	For the processed column in 'upload_file' table, 0 - Uploaded and Not Processed, 1 - Processed and Accepted, 2 - Processed and Rejected
"""