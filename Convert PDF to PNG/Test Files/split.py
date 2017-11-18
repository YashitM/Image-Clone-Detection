from PyPDF2 import PdfFileWriter, PdfFileReader

import time

start = time.time()

inputpdf = PdfFileReader(open("test.pdf", "rb"))

for i in xrange(inputpdf.numPages):
	output = PdfFileWriter()
	output.addPage(inputpdf.getPage(i))
	with open("document-page%s.pdf" % i, "wb") as outputStream:
		output.write(outputStream)

print(time.time() - start)