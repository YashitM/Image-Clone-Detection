# To Run, python split.py

def split_pdfs(file_name):
	"""
    This scipt will convert single pdf file with multiple pages into individual PDF files
    """

	from PyPDF2 import PdfFileWriter, PdfFileReader
	import time
	import convert_single_file
	import compare_png_with_existing
	import config
	import os

	start = time.time()
	inputpdf = PdfFileReader(open(file_name, "rb"))
	for i in xrange(inputpdf.numPages):
		output = PdfFileWriter()
		output.addPage(inputpdf.getPage(i))
		if not os.path.exists(config.store_split_pdfs):
			os.makedirs(config.store_split_pdfs)
		with open(config.store_split_pdfs+file_name.replace(config.store_main_uploads,"")+"%s.pdf" % i, "wb") as outputStream:
			output.write(outputStream)
		convert_single_file.convert_pdf_to_png(config.store_split_pdfs+file_name.replace(config.store_main_uploads,"")+"%s.pdf" % i)
		if config.keep_split_pdf_pages == 0:
			os.remove(config.store_split_pdfs+file_name.replace(config.store_main_uploads,"")+"%s.pdf" % i)

		# compare_png_with_existing.find_similar_thumbnails(file_name+"%s.pdf"+".png" % i)


	print(time.time() - start)

if __name__ == '__main__':
	# Enter the file name here
	file_name = "testingSmallA.pdf"
	split_pdfs(file_name)
