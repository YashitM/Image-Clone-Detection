def handle_pdf(file_name):
	"""
	Updates the database with the document info of the file along with the
	orientation, height and width of the file passed as argument.
	"""
	import mysql.connector
	# from database import login_info
	from PyPDF2 import PdfFileReader
	import os

	inputpdf = PdfFileReader(open(file_name, "rb"))

	document_info = str(inputpdf.getDocumentInfo())
	xmp_info = str(inputpdf.getXmpMetadata())

	db = mysql.connector.Connect(user="root", password="", database="tbl_uploads", host="localhost")
	cursor=db.cursor()

	w = float(inputpdf.getPage(0).mediaBox.getWidth()) * 0.352
	h = float(inputpdf.getPage(0).mediaBox.getHeight()) * 0.352

	orientation = ""

	if w > h:
		orientation = "Landscape"
	else:
		orientation = "Portrait"

	# sql_query = "INSERT INTO `tbl_uploads` (`pdf_id`, `file_dir`, `file_type`, `file_size`, `file_doc_info`, `date_time_upload`, `hash`, `processed`) VALUES ('0', '" + file_name + "', 'PDF', '" + str(os.path.getsize(file_name)) + "', 'TEST INFO', 'TEST TIME', 'TESTHASH', 'TRUE');"
	sql_query = 'UPDATE tbl_uploads SET file_doc_info = "' + document_info + " " + xmp_info + 'Orientation: ' + orientation + 'Dimension(width, height): ' + str(w) + ', ' + str(h) + ' ", processed="TRUE" WHERE file_dir LIKE "' + file_name + '";'

	cursor.execute(sql_query)
	
	cursor.close()

