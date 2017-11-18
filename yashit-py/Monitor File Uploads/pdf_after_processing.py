def handle_pdf(file_name):

	import mysql.connector
	from database import login_info
	from PyPDF2 import PdfFileReader

	inputpdf = PdfFileReader(open(file_name, "rb"))

	document_info = str(inputpdf.getDocumentInfo())
	xmp_info = str(inputpdf.getXmpMetadata())

	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	w = float(p.mediaBox.getWidth()) * 0.352
	h = float(p.mediaBox.getHeight()) * 0.352

	orientation = ""

	if w > h:
		orientation = "Landscape"
	else:
		orientation = "Portrait"

	sql_query = 'UPDATE tbl_uploads SET file_doc_info = "' + document_info + " " + xmp_info + 'Orientation: ' + orientation + 'Dimension(width, height): ' + str(w) + ', ' + str(h) + ' ", processed="TRUE" WHERE processed="FALSE" AND file_dir LIKE "' + file_name + '";'

	cursor.execute(sql_query)
	
	cursor.close()

