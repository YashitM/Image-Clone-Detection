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

 $q=$conn->query("INSERT INTO tbl_uploads(file,type,size) VALUES('$uploadfile','$file_type','$new_size')"); 
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

