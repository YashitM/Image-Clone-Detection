#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

#!/usr/bin/python
from wand.image import Image
from wand.color import Color
import deepzoom
import os
import argparse
from multiprocessing import Pool
import ConfigParser
from database import login_info
import mysql.connector
import multiprocessing
import tempfile,shutil
import time


def run(configlist):
	"""
	This script will  make tiles using deepzoom package
	"""
	drawingid,pdf_page,img,tile_size,tile_overlap,tile_format,working_dir,outputprefix=configlist[0],configlist[1],configlist[2],configlist[3],configlist[4],configlist[5],configlist[6],configlist[7]

	def tile_generator(tile_size, tile_overlap,tile_format):
		'''
			png to tiles with user give settings
		'''
		print "Processing drawing {0}".format(drawingid)
		tmpdir = tempfile.mkdtemp()
		tmpimg=str(drawingid)+"_image.png"
		tmpdzi=str(drawingid)+"_tmp.dzi"
		image_name = tmpdir+"/"+tmpimg
		dzi_name = tmpdir+"/"+tmpdzi

		with open(image_name, "wb") as img_file:
			img_file.write(img)
		db = mysql.connector.Connect(**login_info)
		cursor=db.cursor()

		print "Writing drawing {0}".format(drawingid)
		creator = deepzoom.ImageCreator(tile_size=250, tile_overlap=2, tile_format=tile_format,image_quality=1, resize_filter="bicubic")
		creator.create(image_name, dzi_name)
		width, height = creator.image.size
		print "Deepzoom tiles created for drawing {0}".format(drawingid)
		cursor.execute("UPDATE drawings SET width=%s, height=%s WHERE drawing_id=%s",(width, height, drawingid))
		db.commit()

		basepath = tmpdir+"/"+str(drawingid)+"_tmp_files"

		for d in os.listdir(basepath):
		           curpath = os.path.join(basepath,d)
		           if os.path.isdir(curpath):
		             for f in os.listdir(curpath):
		               if os.path.isfile(os.path.join(curpath,f)):
		                 with open(os.path.join(curpath,f), "rb") as tile_file:
		                   tile_blob = tile_file.read()
		                   cursor.execute("insert into tiles (drawing_id,deepzoom_id,image) values (%s,%s,%s)",(drawingid, d+'_'+f[:-4], tile_blob))
		                   db.commit()
		shutil.rmtree(tmpdir)
		db.close()


	tile_generator(tile_size=tile_size, tile_overlap=tile_overlap,tile_format=tile_format)


def main():

	p = Pool(2)
	while True:
		print "tile_proc iteration"
		config_list=[]
		db = mysql.connector.Connect(**login_info)
		cursor=db.cursor()
		#Read data from database drawings
		cursor.execute("SELECT drawing_id,page_number,image FROM drawings WHERE width IS NULL ORDER BY drawing_id")
#	if not cursor.rowcount:
#		exit()
#	else:

		for row in cursor.fetchall():
			i=row+(250,2,'png',"/var/www/html/","Drawings")
			config_list.append(i)


		db.close()
		#p = Pool(multiprocessing.cpu_count())
		p.map(run, config_list )
	
		time.sleep(2)



if __name__ == '__main__':
	main()
