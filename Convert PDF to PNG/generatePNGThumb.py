from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
import io
import base64
from wand.image import Image
from wand.color import Color
import tempfile
import time

def genPNGThumb(filePath):
	size = 128, 128
	out = filePath + "_thumb.png"
	im = Image.open(filePath)
	im.thumbnail(size, Image.ANTIALIAS)
	im.save(out, "PNG")

def genPDFThumb(pdf_file_name):
	inputpdf = PdfFileReader(pdf_file_name)
	if inputpdf.numPages:
		for i in xrange(inputpdf.numPages):
			output = PdfFileWriter()
			pdf_page = inputpdf.getPage(i)
			output.addPage(pdf_page)
			temp_image = io.BytesIO()
			output.write(temp_image)
			temp_image.seek(0)

			pdf_width, pdf_height = inputpdf.getPage(i).mediaBox[2], inputpdf.getPage(0).mediaBox[3]

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
					bg.save(filename=pdf_file_name.split("/")[len(pdf_file_name.split("/"))-1] + "_image.png")

genPDFThumb("./Test Files/DDA Brochure 2017.pdf")