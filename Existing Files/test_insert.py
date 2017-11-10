from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import base64
from wand.image import Image
from wand.color import Color
import tempfile
import time
import sys
start = time.time()
inputpdf = PdfFileReader(sys.argv[1])

if inputpdf.numPages:
	for i in xrange(inputpdf.numPages):
		output = PdfFileWriter()
		pdf_page = inputpdf.getPage(i)
		output.addPage(pdf_page)
		temp_image = io.BytesIO()
		output.write(temp_image)
		temp_image.seek(0)

		pdf_width, pdf_height = inputpdf.getPage(i).mediaBox[2], inputpdf.getPage(0).mediaBox[3]
		
		print(pdf_width)

		tmpdir = tempfile.mkdtemp()
		tmppdf="lol.pdf"
		pdf_page_name = tmpdir+"/"+tmppdf
		with open(pdf_page_name, "wb") as pdf:
		 output.write(pdf)
		with open(pdf_page_name, "rb") as pdf:
		 rpdf_page=base64.b64encode(pdf.read())
		with Image(file=temp_image,  resolution=50) as img:
			with Image(width=img.width, height=img.height, background=Color("white")) as bg:
				bg.composite(img,0,0)
				png_bin=bg.make_blob('png')
				bg.save(filename=sys.argv[2])

print(time.time() - start)