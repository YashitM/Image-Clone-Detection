from PIL import Image

image = Image.open("1 Drawing-1.png")
image = image.resize((800, 532), Image.ANTIALIAS)
quality_val = 100
image.save("resized.png", 'PNG', quality=quality_val)