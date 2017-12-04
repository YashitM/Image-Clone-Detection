<?php
date_default_timezone_set("Asia/Jakarta");

$servername = "94.101.227.79";
$username = "albums";
$password = "DPyBBfMZgZvfIv8!";
$dbname = "albums"; 
 
// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) 
{
    die("Connection failed: " . $conn->connect_error);
}
//define('BASE_URL','http://zerones.in/client/khalik/image/');
?>
