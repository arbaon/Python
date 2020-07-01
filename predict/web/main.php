<?php
  if (isset($_GET['logout'])) {
	session_destroy();
	}
  if (isset($_POST['user'])) {
	$user=$_POST['user'];
	$_SESSION['user']=$user;
	}
  else if(isset($_SESSION['user'])) {
	  $user=$_SESSION['user'];
	}
   else {
	  $user="none";
	}
  if (isset($_POST['pass'])) {
	$pass=$_POST['pass'];
	$_SESSION['pass']=$pass;
	}
  else if(isset($_SESSION['pass'])) {
	  $pass=$_SESSION['pass'];
	}
   else {
	  $pass="none";
	}
$TV=0;
  if (isset($_POST["view"])) {
    $other=$_POST["view"];
    $_SESSION['other']=$other;
    $TV=1;
  }
  else {
    if (isset($_GET['other'])) {
      $other=$_GET['other'];
      $_SESSION['other']=$other;
    }
    else if (isset($_SESSION['other'])) {
      $other=$_SESSION['other'];
    }
    else {
      $other="none";
    }
  }

  if (isset($_POST["league"])) {
    $league=$_POST["league"];
    $_SESSION['league']=$league;
  }
  if (isset($_GET["league"])) {
    $league=$_GET["league"];
    $_SESSION['league']=$league;
  }
  else if (isset($_SESSION['league'])) {
    $league=$_SESSION['league'];
  }
  else {
    $league="E0";
    $divname="Premier";
  }
  if (isset($_POST["year"])) {
    $year=$_POST["year"];
    $_SESSION['year']=$year;
  }
  else if (isset($_SESSION['year'])) {
    $year=$_SESSION['year'];
  }
  else {
    $year="2018";
  }
  if (isset($_GET['tb'])) {
    $ctable=$_GET['tb'];
    $_SESSION['tb']=$ctable;
    if ($TV<1) { $other="none"; }
  }
  else if (isset($_SESSION['tb'])) {
    $ctable=$_SESSION['tb'];
  }
  else {
    $ctable="league";
  }
  if (isset($_GET['id'])) {
    $csort=$_GET['id'];
      if ($_SESSION['id'] == $csort) {
        if ($_SESSION['srt']=="ASC") { $asort="DESC"; }
	else { $asort="ASC"; }
	}
    $_SESSION['id']=$csort;
    $_SESSION['srt']=$asort;
  }
  else if (isset($_SESSION['id'])) {
    $csort=$_SESSION['id'];
  }
  else {
    switch($ctable) {
      case "league":
    	$csort="pos";
      case "form":
	$csort="pos";
      case "perform":
	$csort="hwtop";
      case "play":
	$csort="pc_goals_t";
      case "weight":
	$csort="pts";
    }
  }
  if (!isset($_SESSION['srt'])) { $asort="DESC"; $_SESSION['srt']==$asort; }
  else { $asort=$_SESSION['srt']; } 
  if (isset($_POST["team1"])) {
    $teama=$_POST["team1"];
    $_SESSION['team1']=$teama;
  }
  else if (isset($_GET['team1'])) {
    $teama=$_GET['team1'];
    $_SESSION==$_GET['team1'];
  }
  else if (isset($_SESSION['team1'])) {
    $teama=$_SESSION['team1'];
  }
  else {
    $teama="none";
  }
  if (isset($_POST["team2"])) {
    $teamb=$_POST["team2"];
    $_SESSION['team2']=$teamb;
  }
  else if (isset($_GET['team2'])) {
    $teamb=$_GET['team2'];
    $_SESSION==$_GET['team2'];
  }
  else if (isset($_SESSION['team2'])) {
    $teamb=$_SESSION['team2'];
  }
  else {
    $teamb="none";
  }
  $MAIN_TABLE=$year."_".$ctable."_table";
?>
