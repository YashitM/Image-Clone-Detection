def convert_pdf_to_png(filename):
	import time
	start = time.time()
	from wand.image import Image
	from wand.color import Color
	from PIL import Image as pilImage

	height = 500

	with Image(filename=filename, resolution=100) as img:
		with Image(width=img.width, height=img.height, background=Color("white")) as bg:
			bg.composite(img,0,0)
			bg.save(filename=filename+".png")

	image = pilImage.open(filename+".png")
	width, height = image.size
	newHeight = 500.0
	factor = newHeight/height
	newWidth = width*factor
	print(newWidth, newHeight)
	image.thumbnail((newWidth,newHeight), pilImage.ANTIALIAS)
	image.save(filename,"PNG")
	print(time.time() - start)

if __name__ == '__main__':
	import os
	directory = "basedir/"
	all_files = os.listdir(directory)
	for i in all_files:
		convert_pdf_to_png(directory + i)