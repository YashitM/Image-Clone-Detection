from PIL import Image

image_1 = 'testImg_scene a.jpg'
image_2 = 'testImg_scene a2.jpg'

import time


start = time.time()
im1 = Image.open(image_1)
rgb_im1 = im1.convert("RGB")

im2 = Image.open(image_2)
rgb_im2 = im2.convert("RGB")

width, height = im1.size

total_pixels = width*height
similar_pixels = 0
for i in range(width):
	for j in range(height):
		r1,g1,b1 = rgb_im1.getpixel((i,j))
		r2,g2,b2 = rgb_im2.getpixel((i,j))

		if r1==r2 and g1==g2 and b1==b2:
			similar_pixels += 1
end = time.time()
print("Time taken: " + str(end-start))
print((similar_pixels/total_pixels)*100)


