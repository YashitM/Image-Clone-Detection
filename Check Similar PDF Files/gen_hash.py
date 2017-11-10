# Need to add this to database as a column

def convert_to_hash(pdf_file_name):
	import hashlib

	BUF_SIZE = 65536

	sha256 = hashlib.sha256()

	with open(pdf_file_name, 'rb') as f:
		while True:
			data = f.read(BUF_SIZE)
			if not data:
				break
			sha256.update(data)
			
	return sha256.hexdigest()

