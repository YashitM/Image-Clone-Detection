<?php
	$targetDir = 'uploads/';
	if (!empty($_FILES)) {
		$targetFile = $targetDir.time().'-'. $_FILES['file']['name'];
		$finfo = finfo_open(FILEINFO_MIME_TYPE);
        $mime = finfo_file($finfo, $_FILES['file']['tmp_name']);
        if (strcmp($mime, 'application/pdf') === 0){
		    move_uploaded_file($_FILES['file']['tmp_name'],$targetFile);
        }
	}
?>