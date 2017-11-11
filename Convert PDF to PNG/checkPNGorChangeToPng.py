import imghdr
from PIL import Image
import os

imageDir = "./"

def checkFile(fileName):
	filePath = imageDir + fileName
	print imghdr.what(filePath)
	if imghdr.what(filePath) != None:
		if (imghdr.what(filePath) != 'png'):
			changeToPngAndSave(filePath)
			deleteExisting(filePath)

def changeToPngAndSave(filePath):
	im = Image.open(filePath)
	im.save(filePath.split("/")[-1].split(".")[0]+'.png')

def deleteExisting(filePath):
	os.remove(filePath)

checkFile('E.jpg')