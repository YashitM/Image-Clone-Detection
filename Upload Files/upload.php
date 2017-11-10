<?php
	$targetDir = 'uploads/';
	if (!empty($_FILES)) {
		$targetFile = $targetDir.time().'-'. $_FILES['file']['name'];
		move_uploaded_file($_FILES['file']['tmp_name'],$targetFile);
	}
?>