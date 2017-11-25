from PIL import Image as pilImage
image = pilImage.open("E.png")
width, height = image.size
newHeight = 500
factor = newHeight/height
newWidth = width*factor
image.thumbnail((newWidth,newHeight), pilImage.ANTIALIAS)
image.save("image.png","PNG")