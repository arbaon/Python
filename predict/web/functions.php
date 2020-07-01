<?php
function username($username,$password) {
  global $conn;
  $username = stripslashes($username);
  $password = stripslashes($password);
  $query=$conn->prepare("select * from Results.login where username='".$username."'");
  $query->execute();
  $result = $query->fetchAll();
  if ($username=$result[0][1]) {
	$checkpass=password_verify($password,$result[0][2]);
      if ($checkpass > 0) {
		$exist=1;
		}
		else {
		$exist=0;
		}
	}
  else {
	$exist=0;
	}
  return $exist;
}
function division_array() {
  $result=ret_query_arr("SELECT CID,Shortname,Longname,Country,Members,Promoted,Relegated from Results.competitions");
  return $result;
}
function year_array() {
  $result=ret_query_arr("SELECT yr1,yr2,yr3,yr4,yr5 from Results.teams limit 1");
  return $result;
}
function team_array($dvn) {
  $result=ret_query_arr("SELECT team from Results.teams where lg1='".$dvn."' order by team asc");
  return $result;
}

function ret_query_arr($QUERY) {
  global $conn;
  $prep = $conn->prepare($QUERY);
  $prep->execute();
  $result = $prep->fetchAll();
  return $result;
}
function display_table($league,$table,$type,$order,$asort)
{
    global $conn;
    global $divname;
    $query=$conn->prepare("select * from Leagues.".$table." where dvn='".$league."' order by ".$order." ".$asort."");
    $query->execute();
    $describe=$conn->prepare("describe ".$table);
    $describe->execute();
    $column=$describe->fetchAll();
    $result = $query->fetchAll();
    $title=$type." Table";
    $cell="cell cell1";
    $tab=$type;
    echo '<div class="table"><div class="Title"><p>'.$divname.' '.$title.'</p></div>
    <div class="heading">';
	foreach ($column as $tow) {
	  if ( $tow[0] != "Dvn" ) {
	    echo '<div class="'.$cell.'"><p><a href=/?id='.$tow[0].'&tb='.$tab.'>'.$tow[0].'</a></p></div>';
	    }
	} 
    echo '</div>';
	foreach ($result as $row) {
            echo '<div class="row">';
	    foreach(range(1, $query->columnCount() - 1) as $ind) {
	      echo '<div class="'.$cell.'"><p>'.$row[$ind].'</p></div>';
		}
	    echo '</div>';
	} 
     echo "</div>";
}
function display_team_table($league,$table,$type,$teama,$teamb)
{
    global $conn;
    global $divname;
    if ($type == "hva") {
      $q_content="Team, if(Team=\"".$teama."\",H_P,A_P) as P,if(Team=\"".$teama."\",H_W,A_W) as W,if(Team=\"".$teama."\",H_D,A_D) as D,if(Team=\"".$teama."\",H_F,A_F) as F,if(Team=\"".$teama."\",H_A,A_A) as A,if(Team=\"".$teama."\",HPS,APS) as PT from Leagues.".$table." where Team=\"".$teama."\" or Team=\"".$teamb."\"";
      }
    else {
      $q_content="* from Leagues.".$table." where dvn=\"".$league."\" and team=\"".$teama."\" or team=\"".$teamb."\"";
    }
    $query=$conn->prepare("select ".$q_content.";");
    $query->execute();
    $result = $query->fetchAll();
    $title=$type." Table";
    $cell_a="cell cell1";
    $cell_b="cell cell1";
    $tab=$type;
    echo '<div class="table"><div class="Title"><p>'.$divname.' '.$title.'</p></div>
    <div class="heading">
    <div class="cell cell1">Stats</div>
    <div class="cell cell1">H Team</div>
    <div class="cell cell1">A Team</div>
    </div>';
      foreach(range(0, $query->columnCount() - 1) as $ind) {
        $meta[]= $query->getColumnMeta($ind);
     	  if ( $meta[$ind]["name"] != "Dvn" ) {
	    if ( $meta[$ind]["name"] !="Team" ) {
	      if ( $result[0][$ind] > $result[1][$ind]) {
	        $cell_a="cell cell6"; $cell_b="cell cell3";
	        }
	      elseif ($result[1][$ind] > $result[0][$ind]) {
	        $cell_a="cell cell3"; $cell_b="cell cell6";
	        }
	      //if ($column[$ind][0] == "Pos") {
	      if ($meta[$ind]["name"] == "Pos") {
	        $cell_tmp=$cell_a; $cell_a=$cell_b;$cell_b=$cell_tmp;
	        }
	      }
	      echo '<div class="row">';
	      echo '<div class="cell cell1"><p>'.$meta[$ind]["name"].'</p></div>';
	      echo '<div class="'.$cell_a.'"><p>'.$result[0][$ind].'</p></div>';
	      echo '<div class="'.$cell_b.'"><p>'.$result[1][$ind].'</p></div>';
	      echo '</div>';
              }
	}
    echo '</div>';	
}
function team_display($league,$year,$teama,$teamb)
{
if ($teama == "none")
  {
    if ($teamb == "none") { echo '<div style="color:red; align:center"><H1>No Teams Selected</H1></div>'; return; }
    else { $teama=$teamb; }
  }
else 
  {
  if ($teamb == "none") { $teamb=$teama; }
  }
  $teama_output=graph($teama);
  $teamb_output=graph($teamb);
  include "graph.php";
  echo '<div>'; // one
    //echo '<div class="table"><div class="row"><div class="cell cell0"><a href="/">Tables</a><br/></div></div></div>';
    echo '<div class="table">'; // two
      echo '<div class="row">'; // three
        echo '<div class="cell cell0">'; // four
         team_results($teama,"H_Team");
         team_results($teamb,"A_Team");
        echo '</div>'; // four
          echo '<div class="cell cell0">';   
            team_results($teama,"D_Team");
             team_results($teamb,"D_Team");
          echo '</div>'; //four
        echo '<div class="cell cell0">';   
          //get_team_data("vs_league");
	  display_team_table($league,$year."_league_form_table","hva",$teama,$teamb);
          echo '<br/>';
          //get_team_data("vs_recent");
    	  echo '<div id="teama_chart" style="width: 300px; height: 150px"></div>';
    	  echo '<div id="teamb_chart" style="width: 300px; height: 150px"></div>';
      echo '</div></div>'; //four three
      echo '<div class="row">'; //three
        echo '<div class="cell cell0">'; //four   
          display_team_table($league,$year."_league_table","league",$teama,$teamb);
        echo '</div>'; //four
        echo '<div class="cell cell0">'; //four   
          display_team_table($league,$year."_form_table","form",$teama,$teamb);
        echo '</div>'; //four
        echo '<div class="cell cell0">'; //four
          display_team_table($league,$year."_perform_table","perform",$teama,$teamb);
        echo '</div></div>';// four three
      echo '<div class="row">'; //three
        echo '<div class="cell cell0">'; //four
          display_team_table($league,$year."_weight_table","weight",$teama,$teamb);
        echo '</div>'; //four
        echo '<div class="cell cell0">'; //four
          display_team_table($league,$year."_play_table","play",$teama,$teamb);
        echo '</div>'; //four
        echo '<div class="cell cell0">'; //four
          predict_vs_table($league,$teama,$teamb);
        echo '</div></div>'; //four three
    echo '</div></div>'; //two one
}
function team_results($team,$type)
{
    global $conn;
    $cell="cell cell1";
    if ($type == "D_Team") 
      { 
	$q1_string="";
	$q2_string="if(H_Team = \"".$team."\",\"H\",\"A\") as FX,if(H_Team !=\"".$team."\",H_Team,A_Team) as Team, if(H_Team = \"".$team."\",if(tmp.R = \"H\",\"W\",if(tmp.R=\"D\",\"D\",\"L\")),if(tmp.R = \"A\",\"W\",if(tmp.R=\"D\",\"D\",\"L\"))) as R,if(H_Team=\"".$team."\",tmp.F,tmp.A) as F, if (A_Team=\"".$team."\",tmp.F,tmp.A) as A,if (H_Team != \"".$team."\",hpos.pos,apos.pos)"; 
      }
    elseif ($type == "H_Team")
      { 
	$q1_string="where ".$type."=\"".$team."\""; 
        $q2_string="tmp.A_Team as Team,if(tmp.R=\"H\",\"W\",if(tmp.R=\"A\",\"L\",\"D\")) as R,tmp.F,tmp.A,apos.pos";
      }
    else
      {
	$q1_string="where ".$type."=\"".$team."\"";
        $q2_string="tmp.H_Team as Team,if(tmp.R=\"A\",\"W\",if(tmp.R=\"H\",\"L\",\"D\")) as R,tmp.A as F,tmp.F as A,hpos.pos";
      }
    $query=$conn->prepare("select * from (select KO,".$q2_string." as Pos from (select KO, H_Team, A_team, R, F ,A from Teams.`".$team."` ".$q1_string." order by KO desc limit 6) as tmp left join Leagues.2017_league_table as hpos on tmp.H_Team = hpos.Team left join Leagues.2017_league_table as apos on tmp.A_Team = apos.Team) as ttbl order by KO desc;");
    $query->execute();   
    $result = $query->fetchAll();
    echo '<div class="table"><div class="Title"><p>'.$team.'</p></div><div class="heading">';
    foreach(range(0, $query->columnCount() - 1) as $column_index)
      {	
    	$meta[]= $query->getColumnMeta($column_index);
        echo '<div class="cell cell1"><p>'.$meta[$column_index]["name"].'</p></div>';
      }
    echo '</div>';
    foreach ($result as $row) {
      echo '<div class="row">';
        foreach(range(0, $query->columnCount() - 1) as $ind) {
          if ($row["R"] == "W") { $cell="cell cell6"; }
 	  elseif ($row["R"] == "D") { $cell="cell cell3"; }
	  else { $cell="cell cell5"; }
          echo '<div class="'.$cell.'"><p>'.$row[$ind].'</p></div>';
           }
         echo '</div>';
        }
    echo '</div>';
}
function graph($team)
{
  $whichos=phpos();
	if ($whichos > 0) {
  		$command = escapeshellcmd('./graph.py "'.$team.'"');
		}
	else {
  		$command = escapeshellcmd('./osx_graph.py "'.$team.'"');
		}
  $output = shell_exec($command);
  return $output;
}
function predict_vs_table($league,$teama,$teamb)
{
 $KO=date("Y-m-d");
  $whichos=phpos();
    if ($whichos > 0) {
 		$command = escapeshellcmd('./compare.py 1 '.$KO.' '.$league.' "'.$teama.'" "'.$teamb.'" "n"');
		}
	else {
 		$command = escapeshellcmd('../osx_compare.py 1 '.$KO.' '.$league.' "'.$teama.'" "'.$teamb.'" "n"');
		}
 $presult = explode(' ',shell_exec($command));
 $prehead = ["lg pos","fm pos","lg perf","fm perf","wgt all","wgt ha","fib","gls","tot"];
  echo '<div class="table"><div class="Title"><p>Predict</p></div>';
  echo '<div class="heading"><div class="cell cell1">Type</div><div class="cell cell1">Predict</div></div>';
  for ($x=0; $x<9; $x++) {
      echo '<div class="row">';
      echo '<div class="cell cell1">'.$prehead[$x].'</div>';
        $cell="cell3";
	if ($presult[$x] < 0 ) { $cell="cell5"; }
        if ($presult[$x] > 0 ) { $cell="cell2"; }
      echo '<div class="cell '.$cell.'">';
      $val=psyn($presult[$x]);
	  //$val=$presult[$x];
      echo $val.'</div></div>';
  }
  echo '</div>';
  
}
function display_predict_table($table)
{
    global $conn;
    $query=$conn->prepare("select * from Predict.".$table);
    $query->execute();
    $describe=$conn->prepare("describe Predict.".$table);
    $describe->execute();
    $column=$describe->fetchAll();
    $result = $query->fetchAll();
    $title=$type." Table";
    $cell="cell cell1";
    $tab=$type;
    echo '<div class="table"><div class="Title"><p>Fixtures</p></div>
    <div class="heading">';
        foreach ($column as $tow) {
          echo '<div class="'.$cell.'"><p><a href=/?id='.$tow[0].'&tb='.$tab.'>'.$tow[0].'</a></p></div>';
        }
    echo '</div>';
        foreach ($result as $row) {
            echo '<div class="row">';
            foreach(range(0, $query->columnCount() -1 ) as $ind) {
    		$cell="cell cell1";
       
		if ($ind > 4 && $ind < 15) {
        	  $cell="cell cell3";
        	  if ($row[$ind] < 0 ) { $cell="cell cell5"; }
        	  if ($row[$ind] > 0 ) { $cell="cell cell2"; }
		}
		if ($ind == 15) { // this is the results column
        	if ($row[$ind] > 0  ) { 
				if ($row[$ind-1] > 0) { $cell="cell cell6"; }
				else {$cell="cell cell5";}
				}
			elseif ($row[$ind] < 0) { 
				if ($row[$ind-1]<0) { $cell="cell cell6"; }
				else { $cell="cell cell5"; }
				}
			else {
				if ($row[$ind-1] == 0) { $cell="cell cell6"; }
				else { $cell="cell cell5"; }
				}
			}
		if ($ind >15) {
		
			switch ($ind) {
				case 16:
					if ($row[$ind] < $row[$ind+1] && $row[$ind] < $row[$ind+2]) { $cell="cell cell2"; } 
					else {$cell="cell cell5";}
				break;
				case 17:
					if ($row[$ind] < $row[$ind-1] && $row[$ind] < $row[$ind+1]) { $cell="cell cell2"; }
					else {$cell="cell cell5";}
				break;
				case 18:
					if ($row[$ind] < $row[$ind-1] && $row[$ind] < $row[$ind-2]) { $cell="cell cell2"; }
					else {$cell="cell cell5";}
				break;
				default:
					$cell="cell cell5";
				break;
				}
			}
        if ( $ind < 1 )
        {
              echo '<div class="'.$cell.'"><p><a href="/?other=teamview&team1='.$row[$ind+3].'&team2='.$row[$ind+4].'&League='.$row[$ind+1].'">'.$row[$ind].'</a></p></div>';
        }
        else {
              echo '<div class="'.$cell.'"><p>'.$row[$ind].'</p></div>';
            }
                }
            echo '</div>';
        }
     echo "</div>";
}
function psyn($val) {
  $rval="D";
	if ( $val > 0 ) {
		$rval="H";
      	if ($val > 1) {
        	$rval=$rval."+";
			if ($val >2) {
	  			$rval=$rval."+";
				if ($val >3) {
	  				$rval=$rval."+";
					}
	  			}
			}
      	}
	if ( $val < 0 ) {
		$rval ="A";
    	if ($val < -1) {
     		$rval=$rval."+";
			if ($val < -2) {
	  			$rval=$rval."+";
				if ($val < -3) {
	  				$rval=$rval."+";
					}
				}
      		}
    	}
return $rval;	
}
function phpos() {
    $pos=PHP_OS;
    if ($pos == "Linux") {
        return 1;
        }
    else {
        return 0;
        }
}
?>


