#!/usr/bin/php
<?php
$servername = "localhost";
$username = "passwd";
$password = "Passwd8177!";

try {
    $conn = new PDO("mysql:host=$servername;dbname=Results", $username, $password);
    // set the PDO error mode to exception
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $dbstatus = "Connected successfully";
    }
catch(PDOException $e)
    {
    echo "Connection failed: " . $e->getMessage();
    }

if (! empty($argv[1]))
  {
	if (! empty($argv[2]))   
		{
			$usern=$argv[1];
			$passwd=$argv[2];
			//$passwd="admin";
			//$usern="admin";
			$check_user=check_user_exists($usern);
			if ( ! $check_user) {
				add_user($usern,$passwd);
				echo "User ".$usern." created";
			}
			else {
				echo "User Exists\n";
			}	
		}
	}
function check_user_exists($username) {
	global $conn;
	$username = stripslashes($username);
	$query=$conn->prepare("select * from Results.login where username='".$username."'");
	$query->execute();
	$result = $query->fetchAll();
	if ($query->rowCount() > 0) {
		if ($username==$result[0][1]) {
			$exist=1;
			}
		else {
			$exist=0;
			}
		return $exist;
		}
	else {
		$exist=0;
		}
	return $exist;
	}
function add_user($username,$password) {
	global $conn;
	$username = stripslashes($username);
	$password = stripslashes($password);
	$passwordhash = password_hash($password,PASSWORD_DEFAULT);
	$query=$conn->prepare("insert into Results.login (username,password) values ('".$username."','".$passwordhash."')");
	$query->execute();
	}
?>
