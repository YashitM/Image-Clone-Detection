#!/usr/bin/env python

####!/usr/local/bin/python2.7
"""
Insert pdfs to drawings database.
"""

import mysql.connector
import ConfigParser
import argparse,os
from database import login_info
from multiprocessing import Pool
from wand.image import Image
from wand.color import Color
import deepzoom
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import multiprocessing
import tempfile
import base64
from StringIO import StringIO
import time

def run(configlist):
	"""
	This script will convert single pdf file into png 
	"""

	pdf_id,pdf_file,file_type,pdf_size,resolution=configlist[0],configlist[1],configlist[2],configlist[3],configlist[4]
	
	def pdf_to_png(pdf_name, res,file_no):
		'''
			Pdf to png convertion at the user given resolution
		'''
		print "processing ", pdf_name
		db = mysql.connector.Connect(**login_info)
		cursor=db.cursor()
		#orig_pdf = StringIO(pdf_name)
		#with open(pdf_name, "rb") as orig_pdf:
		inputpdf = PdfFileReader(pdf_name)
		if inputpdf.numPages:
			for i in xrange(inputpdf.numPages):
				output = PdfFileWriter()
				pdf_page = inputpdf.getPage(i)
				output.addPage(pdf_page)
				temp_image = io.BytesIO()
				output.write(temp_image)
				temp_image.seek(0)
				pgn="{0}.{1}.{2}".format("A",str(file_no),str(i))
				tmpdir = tempfile.mkdtemp()
				tmppdf=str(pgn)+".pdf"
				pdf_page_name = tmpdir+"/"+tmppdf
				with open(pdf_page_name, "wb") as pdf:
				 output.write(pdf)
				with open(pdf_page_name, "rb") as pdf:
				 rpdf_page=base64.b64encode(pdf.read())
				with Image(file=temp_image,  resolution=res) as img:
					with Image(width=img.width, height=img.height, background=Color("white")) as bg:
						bg.composite(img,0,0)
						png_bin=bg.make_blob('png')
						cursor.execute("""INSERT INTO drawings(page_number,image,pdf) VALUES (%s,%s, %s)""", (pgn,png_bin,rpdf_page))
						db.commit()
						bg.save(filename=pdf_file_name.split("/")[len(pdf_file_name.split("/"))-1] + "_image.png")

				#rpdf_page.close()
		db.close()

	pdf_to_png(pdf_file,300,pdf_id)



def main():

	proc_allowed=int(multiprocessing.cpu_count())

	if (proc_allowed -1) > 0:
		p = Pool(proc_allowed -1)
	else:
		p=Pool(1)

	while True:
		print "insert iteration"
		config_list=[]
		res=300
		db = mysql.connector.Connect(**login_info)

		cursor=db.cursor()
		#Read data from database drawings
		cursor.execute("SELECT pdf_id,file,type,size FROM tbl_uploads")

#       if cursor.rowcount < 1:
#           print "No uploads found"
#           db.close()
#       else:
#           print "Found %d uploads"%cursor.rowcount
		for row in cursor.fetchall():
			i=row+(res,)
			config_list.append(i)

		cursor.execute("""DELETE FROM tbl_uploads""")
		db.commit()
		db.close()

		p.map(run, config_list)

		time.sleep(2)

if __name__ == '__main__':
	main()
