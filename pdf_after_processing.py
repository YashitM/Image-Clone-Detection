def walk(obj, fnt, emb):
	if not hasattr(obj, 'keys'):
		return None, None
	fontkeys = set(['/FontFile', '/FontFile2', '/FontFile3'])
	if '/BaseFont' in obj:
		fnt.add(obj['/BaseFont'])
	if '/FontName' in obj:
		if [x for x in fontkeys if x in obj]:# test to see if there is FontFile
			emb.add(obj['/FontName'])

	for k in obj.keys():
		walk(obj[k], fnt, emb)

	return fnt, emb# return the sets for each page

def handle_pdf(file_hash, file_name, uploaded_file_id):
	"""
	Updates the database with the document info of the file along with the
	orientation, height and width of the file passed as argument.
	Input: uploaded file
	Output: Update details about the file in 'upload_file' 
	"""
	import sys
	import mysql.connector
	from PyPDF2 import PdfFileReader
	import os
	from database import login_info
	import json
	import config

	inputpdf = PdfFileReader(open(file_name, "rb"))

	document_info = inputpdf.getDocumentInfo()
	xmp_info = inputpdf.getXmpMetadata()
	
	db = mysql.connector.Connect(**login_info)
	cursor=db.cursor()

	w = float(inputpdf.getPage(0).mediaBox.getWidth()) * 0.352
	h = float(inputpdf.getPage(0).mediaBox.getHeight()) * 0.352

	orientation = ""

	if w > h:
		orientation = "Landscape"
	else:
		orientation = "Portrait"

	pdf_info = {}
	fonts = set()
	embedded = set()
	for page in inputpdf.pages:
		obj = page.getObject()
		f, e = walk(obj['/Resources'], fonts, embedded)
		fonts = fonts.union(f)
		embedded = embedded.union(e)

	unembedded = fonts - embedded
	font_list = sorted(list(fonts))

	pdf_info['pages'] = str(inputpdf.numPages)
	pdf_info['orientation'] = orientation
	pdf_info['dimensions'] = {"width": str(w), "height": str(h)}
	pdf_info['fonts'] = font_list

	print(pdf_info)
	
	doc_info = {}
	if document_info!=None:
		for item in document_info:
			doc_info[item] = document_info[item]

	xmp_pdf_info = {}
	if xmp_info!=None:
		for item in xmp_info:
			xmp_pdf_info[item] = xmp_info[item]

	pdf_info['document_information'] = doc_info
	pdf_info['xmp_information'] = xmp_pdf_info

	sql_query = "UPDATE upload_file SET doc_info = '" + (str(json.dumps(pdf_info)).replace('"','\\"')).replace("'","\\'") + "', processed='1' WHERE processed='0' AND hash LIKE '" + file_hash + "';"

	cursor.execute(sql_query)
	db.commit()
	cursor.close()

	print("[" + str(uploaded_file_id) + "] Added PDF details to 'upload_file' table.")
	config.write_to_file(config.log_file_name,"[" + str(uploaded_file_id) + "] Added PDF details to 'upload_file' table.")

if __name__ == '__main__':
	handle_pdf("loooool","uploads/BlankSmall.pdf")
