from PIL import Image

def genPNGThumb(filePath):
	size = 128, 128
	out = filePath + "_thumb.png"
	im = Image.open(filePath)
	im.thumbnail(size, Image.ANTIALIAS)
	im.save(out, "PNG")

# genPNGThumb("./Test Files/E.png")