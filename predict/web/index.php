<?php
session_start();
require "functions.php";
include "main.php";
require "conn.php";
$logon=username($user,$pass);
echo "
<html>
<head>
  <title>Better than OPTA</title>
  <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />
  <link href=\"main.css\" type=\"text/css\" rel=\"stylesheet\" />
</head>
<body>
  <div class=\"content\">
    <div class=\"background main\">
      <div class=\"background left\">
      </div>
    </div>
    <div class=\"center_block main\">
      <div class=\"content\">
	<div class=\"top_block top\">
	  <div class=\"content\">
	    <div class=\"left_block topleft\"><H2> BETTER THAN OPTA</H2></div>
	      <div class=\"background t_item_01\">
	      </div>
	      <div class=\"right_block tright t_item_01\">
		<div class=\"content\">";
		if ($logon > 0) {
			echo "
				</br>
				<center>
				<a href=\"index.php?logout=true\">LOGOUT</a>
				</center>";
		}
		echo "
		</div>
	      </div>
	    </div>
	  </div>
	  <div class=\"left_block left\">
	    <div class=\"content\">
	      <div class=\"top_block item01 item\">
		<a href=\"index.php?id=Pos&tb=league&other=none\"><div class=\"content\">
		  <p>LEAGUE TABLES</p>
	        </div></a>
	      </div>
	      <div class=\"top_block item02 item\">
	        <a href=\"index.php?id=Pos&tb=form\"><div class=\"content\">
	          <p>FORM TABLES</p>
	        </div></a>
	      </div>
	      <div class=\"top_block item03 item\">
		<a href=\"index.php?id=hwt&tb=perform\"><div class=\"content\">
		  <p>PERFORM TABLES</p>
		</div></a>
	      </div>
	      <div class=\"top_block item04 item\">
		<a href=\"index.php?id=pc_goals_t&tb=play\"><div class=\"content\">
		  <p>PLAY TABLES</p>
		</div></a>
	      </div>
	      <div class=\"top_block item05 item\">
		<a href=\"index.php?id=Pts&tb=weight\"><div class=\"content\">
		  <p>WEIGHT TABLE</p>
		</div></a>
	      </div>
	      <div class=\"top_block item06 item\">
		<a href=\"index.php?other=teamview\"><div class=\"content\">
		  <p>TEAM VIEW</p>
		</div></a>
	      </div>
              <div class=\"top_block item07 item\">
                <a href=\"index.php?other=fixtures\"><div class=\"content\">
                  <p>FIXTURES</p>
                </div></a>
              </div>
	      <div class=\"top_block selectitem\">
      		<div class=\"content\">
		  <br />";
		  $div=division_array();
		  $divcount=count($div);
		  echo "<form method=\"post\"><select name=\"league\" onchange=\"this.form.submit()\">";
		  for ( $y=0; $y < $divcount; $y++ ) {
		    echo '<option value='.$div[$y][0].' '; if ( $league == $div[$y][0]) { echo "selected"; $divname=$div[$y][2];} echo '>'.$div[$y][2].'</option>';
		}							
		echo "</select></form>";
		
		$yr=year_array();
		echo "<form method=\"post\"><select name=\"year\" onchange=\"this.form.submit()\">";
                  foreach (range(0, 4) as $X) {		    
	  	    echo '<option value='.$yr[0][$X].' '; if ( $year == $yr[0][$X]) { echo "selected"; } echo '>'.$yr[0][$X].'</option>';
		  }
	        echo"</select></form>";
		echo "<form method=\"post\" onsubmit=\"this.form.submit()\" enctype=\"multipart/form-data\">";
		echo "<select name=\"team1\">";
		echo "<option value=\"none\""; if ( $teama == "none") { echo "selected";} echo "> none </option>";
		$dvnteams=team_array("$league");
                  foreach ($dvnteams as $row) {		    
	  	    echo '<option value="'.$row['team'].'"'; if ( $teama == $row['team']) { echo "selected"; } echo '>'.$row['team'].'</option>';
		  }
		echo "</select>";
		echo "<select name=\"team2\">";
		echo "<option value=\"none\""; if ( $teamb == "none") { echo "selected";} echo "> none </option>";
		$dvnteams=team_array("$league");
                  foreach ($dvnteams as $row) {		    
	  	    echo '<option value="'.$row['team'].'"'; if ( $teamb == $row['team']) { echo "selected"; } echo '>'.$row['team'].'</option>';
		  }
		echo "</select><br /><br />";
		echo "<input type='submit' name='view' value='teamview'>";
		echo "</form>";
		  
	  echo "</div>
	      </div>
	    </div>
	  </div>";
           //MAIN BODY
	//$logon=username($user,$pass);
	if ($logon > 0) {
		echo "<div class=\"window\">";
		if ($other !="none") {
			if ($other == "teamview") { 
				team_display($league,$year,$teama,$teamb);
			}
	     	if ($other == "fixtures") {
				//display_predict_table("predict");
				display_predict_table("predict_view");
				}
 	   		}
	   	else {		
	     		display_table($league,$MAIN_TABLE,$ctable,$csort,$asort);
	   		}
		}
		else {
				echo "
				<div class=\"cell\">
				<center><b>Login Required</b></center></br>
				<form action=\"/index.php\" method=\"post\">
				<label>UserName :</label>
				<input id=\"username\" name=\"user\" placeholder=\"username\" type=\"text\">
				<label>Password :</label>
				<input id=\"password\" name=\"pass\" placeholder=\"**********\" type=\"password\">
				<input name=\"submit\" type=\"submit\" value=\" Login \">
				</form>
				</div>";
			}
	   echo "</div>";
	   echo "
	</div>
      </div>
    </div>
  </div>
<!-- 
 * Layout generated with http://layzilla.com
 * Layout generator is free of use.
 * We appreciate if you leave this comment block in commercial use of generator.
 * All comment and ideas can be submitted to us using contacts below.
 *
 *    site: www.jmholding.lv
 *   email: info@jmholding.lv
 *  twitter: @jmholding_lv
 -->
</body>
</html>
";
?>
