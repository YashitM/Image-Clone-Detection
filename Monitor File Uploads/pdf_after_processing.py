def handle_pdf(file_name):
	"""
	Updates the database with the document info of the file along with the
	orientation, height and width of the file passed as argument.
	"""
	# import mysql.connector
	# from database import login_info
	from PyPDF2 import PdfFileReader
	print("In here" + file_name)

	inputpdf = PdfFileReader(open(file_name, "rb"))

	document_info = str(inputpdf.getDocumentInfo())
	xmp_info = str(inputpdf.getXmpMetadata())

	# db = mysql.connector.Connect(**login_info)
	# cursor=db.cursor()

	w = float(inputpdf.getPage(0).mediaBox.getWidth()) * 0.352
	h = float(inputpdf.getPage(0).mediaBox.getHeight()) * 0.352

	orientation = ""

	if w > h:
		orientation = "Landscape"
	else:
		orientation = "Portrait"

	print(orientation, document_info, xmp_info)

	# sql_query = 'UPDATE tbl_uploads SET file_doc_info = "' + document_info + " " + xmp_info + 'Orientation: ' + orientation + 'Dimension(width, height): ' + str(w) + ', ' + str(h) + ' ", processed="TRUE" WHERE processed="FALSE" AND file_dir LIKE "' + file_name + '";'

	# cursor.execute(sql_query)
	
	# cursor.close()

