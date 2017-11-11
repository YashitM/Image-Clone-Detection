<?php
	require 'init.php';

	$targetDir = 'uploads/';
	if (!empty($_FILES)) {
		$finfo = finfo_open(FILEINFO_MIME_TYPE);
		$mime = finfo_file($finfo, $_FILES['file']['tmp_name']);
		$file_type = "";
		$time_details = date("Y/m/d").date("h:i:sa");
		$modified = filemtime($filename);
		$size = filesize($_FILES['file']['tmp_name']);
		$targetFile = $targetDir.time().'-'. $_FILES['file']['name'];
		$file_hash = hash_file('sha256', $_FILES['file']['tmp_name']);
		
		if (strcmp($mime, 'application/pdf') === 0){
			$file_type = "PDF";
		} else if (strcmp($mime, 'image/png') === 0){
			$file_type = "PNG";
		} else if (strcmp($mime, 'image/jpeg') === 0) {
			$file_type = "JPG";
		} else if (strcmp($mime, 'image/bmp/') === 0) {
			$file_type = "BMP";
		} else {
			$file_type = "OTHER";
		}

		$mysql_query = "INSERT INTO tbl_uploads VALUES ('1', '$targetFile' , '$file_type', '$file_size', 'NONE', '$time_details', '$file_hash', 'FALSE')";
		$result = mysqli_query($con, $mysql_query);
		if ( mysqli_num_rows($result) > 0 ){
			move_uploaded_file($_FILES['file']['tmp_name'],$targetFile);
		}
	}
?>