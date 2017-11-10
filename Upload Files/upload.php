<?php
	$targetDir = 'uploads/';
	if (!empty($_FILES)) {
		$targetFile = $targetDir.time().'-'. $_FILES['file']['name'];
		$finfo = finfo_open(FILEINFO_MIME_TYPE);
        $mime = finfo_file($finfo, $_FILES['file']['tmp_name']);
        if (strcmp($mime, 'application/pdf') === 0){
            $targetDir = $targetDir."PDFs/";
		    move_uploaded_file($_FILES['file']['tmp_name'],$targetFile);
        }
        else if (strcmp($mime, 'image/png') === 0){
            $targetDir = $targetDir."PNGs/";
		    move_uploaded_file($_FILES['file']['tmp_name'],$targetFile);
        } else {
            $targetDir = $targetDir."Others/";
            move_uploaded_file($_FILES['file']['tmp_name'],$targetFile);
        }
	}
?>