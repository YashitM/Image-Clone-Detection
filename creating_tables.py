
from database import login_info
import mysql.connector


db = mysql.connector.Connect(**login_info)
cursor=db.cursor()

cursor.execute("""DROP TABLE IF EXISTS users""")
cursor.execute("""
	CREATE TABLE users(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		email VARCHAR(100),
		pass VARCHAR(100),
		verification_token VARCHAR(100),
		reset_token VARCHAR(100),
		registered_on VARCHAR(100),
		reset_date VARCHAR(100),
		verified BOOLEAN,
		firstname VARCHAR(100),
		lastname VARCHAR(100)
	)
	""")

cursor.execute("""DROP TABLE IF EXISTS album""")
cursor.execute("""
	CREATE TABLE album(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		user_id VARCHAR(100),
		name VARCHAR(100),
		upload_log CLOB,
	)
	""")

cursor.execute("""DROP TABLE IF EXISTS upload_file""")
cursor.execute("""
	CREATE TABLE upload_file(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		timeUploaded VARCHAR(100),
		hash VARCHAR(100),
		type VARCHAR(100),
		size VARCHAR(100),
		doc_info CLOB,
		processed BOOLEAN,
		dir VARCHAR(500),
	)
	""")

cursor.execute("""DROP TABLE IF EXISTS image""")
cursor.execute("""
	CREATE TABLE image(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		album_id VARCHAR(100),
		user_id VARCHAR(100),
		page_size VARCHAR(100),
		png VARCHAR(100),
		pdf VARCHAR(100),
		width VARCHAR(100),
		height VARCHAR(100),
		thumb VARCHAR(100),
		page_number VARCHAR(100),
		request_json CLOB
	)
	""")


cursor.execute("""DROP TABLE IF EXISTS tiles""")
cursor.execute("""
	CREATE TABLE tiles(
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		image_id VARCHAR(100),
		deepzoom_id VARCHAR(100),
		tile VARCHAR(100)
	)
	""")


cursor.execute("""DROP TABLE IF EXISTS thumb_comparision""")
cursor.execute("""
	CREATE TABLE thumb_comparision(
		new_image_id INTEGER PRIMARY KEY AUTOINCREMENT,
		existing_image_id VARCHAR(100),
		comparision VARCHAR(100),
		difference_percentage INTEGER
	)
	""")

def insertInUser(email, passwd, verification_token, reset_token, registered_on, reset_date, verified, firstname, lastname):
	s = email + ", " + passwd + ", " + verification_token + ", " + reset_token + ", " + registered_on + ", " + reset_date + ", " + str(verified) + ", " + firstname + ", " + lastname
	cursor.execute("""
		INSERT INTO users(
			email, pass, verification_token, reset_token, registered_on, reset_date, verified, firstname, lastname
		) VALUES ( """ + s + """ )""")

def insertInAlbum(user_id, name, upload_log):
	s = user_id + ", " + name + ", " + upload_log
	cursor.execute("""
		INSERT INTO album(
			user_id, name, upload_log
		) VALUES ( """ + s + """)""")

def insertInUploadFile(currTime, hashid, typeparam, size, doc_info, processed, dirparam):
	s = currTime + ", " + hashid + ", " + typeparam + ", " + size + ", " + doc_info + ", " + str(processed) + ", " + dirparam
	cursor.execute("""
		INSERT INTO upload_file(
			timeUploaded, hash, type, size,	doc_info, processed, dir
		) VALUES ( """ + s + """)""")

def insertInImage(album_id, user_id, page_size, png, pdf, width, height, thumb, page_number, request_json):
	s = album_id + ", " + user_id + ", " + page_size + ", " + png + ", " + pdf + ", " + width + ", " + height + ", " + thumb + ", " + page_number + ", " + request_json
	cursor.execute("""
		INSERT INTO image(
			album_id, user_id, page_size, png, pdf, width, height, thumb, page_number, request_json
		) VALUES ( """ + s + """)""")

def insertInTiles(image_id, deepzoom_id, tile):
	s = image_id + ", " + deepzoom_id + ", " + tile
	cursor.execute("""
		INSERT INTO image(
			image_id, deepzoom_id, tile
		) VALUES ( """ + s + """)""")

def insertInThumbComparision(existing_image_id, comparision, difference_percentage):
	s = existing_image_id + ", " + comparision + ", " + difference_percentage
	cursor.execute("""
		INSERT INTO image(
			existing_image_id, comparision, difference_percentage
		) VALUES ( """ + s + """)""")

def deleteRowFromTable(table_name, coloumnName, value):
	"""
	Deletes row from given table where the given value equals the value in the coloumn given in coloumnName
	"""

	cursor.execute("""
		DELETE FROM """ + table_name + """ WHERE """ + coloumnName + """ = """ + value
		)

#Remove the table if exists
# cursor.execute("""DROP TABLE IF EXISTS drawings""")
# cursor.execute("""
# 	CREATE TABLE drawings(
# 		drawing_id INTEGER PRIMARY KEY AUTO_INCREMENT,
# 		page_number VARCHAR(10),
# 		image LONGBLOB,
# 		pdf	LONGBLOB,
#                 width INTEGER,
# 		height INTEGER,
# 		request_json VARCHAR(10),
# 		result_json VARCHAR(10)
# 		)
# 	""")

# cursor.execute("""DROP TABLE IF EXISTS tiles""")
# cursor.execute("""
# 	CREATE TABLE tiles(
# 		id INTEGER PRIMARY KEY AUTO_INCREMENT,
# 		drawing_id INTEGER,
# 		deepzoom_id VARCHAR(10),
# 		image LONGBLOB
# 		)
# 	""")


# cursor.execute("""DROP TABLE IF EXISTS tbl_uploads""")
# cursor.execute("""
#         CREATE TABLE tbl_uploads(
#         	pdf_id INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
#                 file  VARCHAR( 100 ) NOT NULL,
#                 type  VARCHAR( 100 ) NOT NULL,
#                 size INT NOT NULL
#                 )
#         """)

# cursor.execute("""DROP TABLE IF EXISTS tbl_uploads_test""")
# cursor.execute("""
#         CREATE TABLE tbl_uploads_test(
#         	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
#             file_dir  VARCHAR( 100 ) NOT NULL,
#             file_type  VARCHAR( 100 ) NOT NULL,
#             file_size INT NOT NULL,
#             file_doc_info VARCHAR( 5000 ) NOT NULL,
#             date_time_uplaod VARCHAR( 5000 ) NOT NULL,
#             hash VARCHAR( 100 ) NOT NULL,
#             processed VARCHAR( 10 ) NOT NULL
#         )
# """)
