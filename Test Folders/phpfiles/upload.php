l<?php
include("dbconfig.php");
if(isset($_POST['btn-upload']))
{    
  
 $file = rand(1000,100000)."-".$_FILES['file']['name'];
 $file_loc = $_FILES['file']['tmp_name'];
 $file_size = $_FILES['file']['size'];
 $file_type = $_FILES['file']['type'];
 $folder="/home/rkampenuss/www/c-ev.com/py/yashit-py/MonitorFileUploads/";
 $uploadfile = $folder . basename($file);
 move_uploaded_file($_FILES["file"]["tmp_name"],$uploadfile);
 
 // new file size in KB
 $new_size = $file_size/1024;  
 // new file size in KB
 
 // make file name in lower case
 $new_file_name = strtolower($file);
 // make file name in lower case

 
 $final_file=str_replace(' ','-',$new_file_name);
 // $file_type = "";
 //  if (strcmp($mime, 'application/pdf') === 0){
 //    $file_type = "PDF";
 //  } else if (strcmp($mime, 'image/png') === 0){
 //    $file_type = "PNG";
 //  } else if (strcmp($mime, 'image/jpeg') === 0) {
 //    $file_type = "JPG";
 //  } else if (strcmp($mime, 'image/bmp/') === 0) {
 //    $file_type = "BMP";
 //  } else {
 //    $file_type = "OTHER";
 //  }

 $file_hash = hash_file('sha256', $_FILES['file']['tmp_name']);
 $time_details = date("Y/m/d").date("h:i:sa");

$q=$conn->query("INSERT INTO tbl_uploads_test VALUES(1,'$uploadfile','$file_type','$new_size','NONE', '$time_details', '$file_hash', 'FALSE')"); 
 if($q)
 {
  ?>
  <script>
 // alert('successfully uploaded');
        window.location.href='index.php?success';
        </script>
  <?php
 }
 else
 {
   echo 'Here is some more debugging info:';
   print_r($_FILES);
  ?>
  <script>
  alert('error while uploading file');
        window.location.href='index.php?fail';
  </script>
  <?php
 }
}
?>

