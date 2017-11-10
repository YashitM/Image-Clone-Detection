<?php
	$targetDir = 'uploads/';
	if (!empty($_FILES)) {
		$finfo = finfo_open(FILEINFO_MIME_TYPE);
		$mime = finfo_file($finfo, $_FILES['file']['tmp_name']);
		if (strcmp($mime, 'application/pdf') === 0){
			$targetFile = $targetDir.'PDFs/'.time().'-'. $_FILES['file']['name'];
			move_uploaded_file($_FILES['file']['tmp_name'],$targetFile);
		}
		else if (strcmp($mime, 'image/png') === 0){
			$targetFile = $targetDir.'PNGs/'.time().'-'. $_FILES['file']['name'];
			move_uploaded_file($_FILES['file']['tmp_name'],$targetFile);
		} else if (strcmp($mime, 'image/jpeg') === 0) {
			$targetFile = $targetDir.'JPEGs/'.time().'-'. $_FILES['file']['name'];
			move_uploaded_file($_FILES['file']['tmp_name'],$targetFile);
		} else if (strcmp($mime, 'image/bmp/') === 0) {
			$targetFile = $targetDir.'BMPs/'.time().'-'. $_FILES['file']['name'];
			move_uploaded_file($_FILES['file']['tmp_name'],$targetFile);
		} else {
			$targetFile = $targetDir.'Others/'.time().'-'. $_FILES['file']['name'];
			move_uploaded_file($_FILES['file']['tmp_name'],$targetFile);
		}
	}
?>