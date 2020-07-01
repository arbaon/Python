<?php
$servername = "localhost";
$username = "php";
$password = "Php8177!";

try {
    $conn = new PDO("mysql:host=$servername;dbname=Leagues", $username, $password);
    // set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $dbstatus = "Connected successfully"; 
    }
catch(PDOException $e)
    {
    echo "Connection failed: " . $e->getMessage();
    }
?>
