<?php
date_default_timezone_set("PST");
$servername = "94.101.227.79";
$dbname = "albums_yashit"; 
$username = "albums";
$password = "DPyBBfMZgZvfIv8!";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) 
{
    die("Connection failed: " . $conn->connect_error);
}
//define('BASE_URL','http://zerones.in/client/khalik/image/');
?>
