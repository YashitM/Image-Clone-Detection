
def handle_pdf(file_hash, file_name):
	"""
	Updates the database with the document info of the file along with the
	orientation, height and width of the file passed as argument.
	"""
	import sys
	import mysql.connector
	from PyPDF2 import PdfFileReader
	import os
	from database import login_info
	inputpdf = PdfFileReader(open(file_name, "rb"))

	document_info = str(inputpdf.getDocumentInfo())
	xmp_info = str(inputpdf.getXmpMetadata())

	# db = mysql.connector.Connect(user="root", password="", database="tbl_uploads", host="localhost")
	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	w = float(inputpdf.getPage(0).mediaBox.getWidth()) * 0.352
	h = float(inputpdf.getPage(0).mediaBox.getHeight()) * 0.352

	orientation = ""

	if w > h:
		orientation = "Landscape"
	else:
		orientation = "Portrait"

	s = "Pages:" + str(inputpdf.numPages) + ", " + document_info + ", " + xmp_info + 'Orientation:' + orientation + 'Dimension(width, height):' + str(w) + ',' + str(h)
	s = s.replace("'","")
	s = s.replace('"','')
	# sql_query = """INSERT INTO `tbl_uploads_test` (`file_id`, `file_dir`, `file_type`, `file_size`, `file_doc_info`, `date_time_upload`, `hash`, `processed`) VALUES ('0', '""" + file_name + """', 'PDF', '""" + str(os.path.getsize(file_name)) + """', '""" + s + """', 'TEST TIME', 'TESTHASH', 'TRUE');"""
	# sql_query = 'UPDATE tbl_uploads_test SET file_doc_info = "' + s  ' ", processed="TRUE" WHERE file_dir LIKE "' + file_name + '";'
	sql_query = "UPDATE tbl_uploads_test SET file_doc_info = '" + s + "', processed='TRUE' WHERE hash LIKE '" + file_hash + "';"

	cursor.execute(sql_query)
	
	cursor.close()

