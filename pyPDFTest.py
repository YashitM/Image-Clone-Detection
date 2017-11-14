import PyPDF2
import mysql.connector
from database import login_info
import os


def PdfinfoToDb(filePath):
	"""
	Returns width, height of the Pdf file in millimeters.
	"""
	pdf = PyPDF2.PdfFileReader(filePath, "rb")
	p = pdf.getPage(1)

	w = float(p.mediaBox.getWidth()) * 0.352
	h = float(p.mediaBox.getHeight()) * 0.352

	db = mysql.connector.Connect()
	cursor=db.cursor()

	s = "Dimension is width = " + str(w) + " height = " + str(h) 

	cursor.execute("UPDATE tbl_uploads SET file_doc_info = " + s + " WHERE hash = " + myhash + ";")

	cursor.close()
