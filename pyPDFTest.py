import PyPDF2
import mysql.connector
from database import login_info
import os


def PdfinfoToDb(filePath):
	"""
	Updates the database with the orientation, height, width of the PDF file given as parameter.
	"""
	pdf = PyPDF2.PdfFileReader(filePath, "rb")
	p = pdf.getPage(0)

	w = float(p.mediaBox.getWidth()) * 0.352
	h = float(p.mediaBox.getHeight()) * 0.352

	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	orientation = ""

	if w > h:
		orientation = "Landscape"
	else:
		orientation = "Portrait"

	s = "Orientation: " + orientation + " Dimension: width = " + str(w) + " height = " + str(h)

	cursor.execute("UPDATE tbl_uploads SET file_doc_info = " + s + " WHERE hash = " + myhash + ";")

	cursor.close()
