# To Run, python split.py

def split_pdfs(file_name):
	"""
    This scipt will convert single pdf file with multiple pages into individual PDF files
    """

	from PyPDF2 import PdfFileWriter, PdfFileReader
	import time

	start = time.time()

	inputpdf = PdfFileReader(open(file_name, "rb"))

	for i in xrange(inputpdf.numPages):
		output = PdfFileWriter()
		output.addPage(inputpdf.getPage(i))
		with open("basedir/document-page%s.pdf" % i, "wb") as outputStream:
			output.write(outputStream)

	print(time.time() - start)

if __name__ == '__main__':
	# Enter the file name here
	file_name = "test.pdf"
	split_pdfs(file_name)