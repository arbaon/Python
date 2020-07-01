#/bin/sh
# pass in the file name as an argument: ./mktable filename.csv

NEXT_SEASON="2018"
CURR_SEASON="2017"
LAST_SEASON="2016"
LST1_SEASON="2015"
LST2_SEASON="2014"
LST3_SEASON="2013"
LST4_SEASON="2012"
USER="root"
PASS=""
DB="Results"
DBT="Teams"
DBL="Leagues"
DBP="Predict"
PWDIR=$(pwd)
INT=0
UPD=0
HST=0

function upload_csv {
sudo cp $1 /tmp/
mysql -u$USER $DB -e "LOAD DATA INFILE \"/tmp/$1\" INTO TABLE $2 COLUMNS TERMINATED BY \",\" IGNORE 1 LINES"
sudo rm /tmp/$1
}

function pull_data {
  download_league $CURR_SEASON
  download_league $LAST_SEASON
  download_league $LST1_SEASON
  download_league $LST2_SEASON
  download_league $LST3_SEASON
}

function download_league {
FP=$(($1 - 2000));LP=$((FP + 1));SN=$FP$LP

if [ -d "$PWDIR/data/seasons/$1" ]; then
  rm -rf $PWDIR/data/seasons/$1
fi
mkdir -p $PWDIR/data/seasons/$1
cd $PWDIR/data/seasons/$1
for LIST in E0 E1 E2 E3 EC D1 D2 I1 I2 F1 F2 B1 P1 N1 SP1 SP2 SC0 SC1 SC2 SC3 G1 T1
  do
    wget http://www.football-data.co.uk/mmz4281/$SN/$LIST.csv
  done
}

function create_db {
mysql -u$USER -e "DROP DATABASE IF EXISTS $1"
mysql -u$USER -e "CREATE DATABASE $1"
}
function create_table {
  printf "create table $2( " > $2.sql	
  head -1 $1 | sed -e 's/Div/Divn/g' | sed -e 's/>2.5/gt25/g' | sed -e 's/<2.5/lt25/g' | sed -e 's/,/ varchar(35),/g' >> $2.sql
  printf " varchar(35));" >> $2.sql
  sed -i '' "s/Kickoff varchar(35)/Kickoff date/" $2.sql
}
function create_db_accounts {
 mysql -u$USER $DB -e "create table login (id int not null auto_increment,username varchar(20),password varchar(128),primary key (id))"
 mysql -u$USER mysql -e "grant all privileges on Results.* to 'passwd'@'%' identified by 'Passwd8177!'"
 mysql -u$USER mysql -e "grant all privileges on *.* to 'python'@'%' identified by 'Python8177!'"
 mysql -u$USER mysql -e "grant SELECT on Results.* to 'php'@'%' identified by 'Php8177!'"
 mysql -u$USER mysql -e "grant SELECT on Teams.* to 'php'@'%' identified by 'Php8177!'"
 mysql -u$USER mysql -e "grant SELECT on Leagues.* to 'php'@'%' identified by 'Php8177!'"
 mysql -u$USER mysql -e "grant SELECT on Results.* to 'php'@'%' identified by 'Php8177!'"
 mysql -u$USER mysql -e "grant SELECT on Predict.* to 'php'@'%' identified by 'Php8177!'"
 mysql -u$USER mysql -e "flush privileges"
}
function create_competition {
  WDIR=$(pwd)
  create_table $1 $1
    for VC in Members Promoted Relegated Template
    do
      sed -i '' "s/$VC varchar(35)/$VC int/" $1.sql
    done
  mysql -u$USER $DB -e "DROP TABLE IF EXISTS $1"
  mysql -u$USER $DB < $1.sql
  upload_csv $1 $1
  rm $1.sql
}

function upload_fixtures {
  WDIR=$(pwd)
  NAME=$(echo $1 | cut -d'.' -f1)
  create_table $1 TMP_$2_$NAME
  for VC in FTHG FTAG HTHG HTAG HOS AWS HOST AWST HF AF HC AC HY AY HR AR
    do
      sed -i '' "s/$VC varchar(35)/$VC int/" TMP_$2_$NAME.sql
    done
  mysql -u$USER $DB -e "DROP TABLE IF EXISTS TMP_$2_$NAME"
  mysql -u$USER $DB < TMP_$2_$NAME.sql
  upload_csv $1 TMP_$2_$NAME
  rm TMP_$2_$NAME.sql
}
function clean_csv {
  if [ "$1" == "EC" ]; then
    mv $1.csv $1_tmp.csv
    iconv -c -f utf-8 -t ascii $1_tmp.csv > $1.csv
    rm $1_tmp.csv
  fi
  mv $1.csv $1_tmp.csv
  cat $1_tmp.csv | egrep -v "^," > $1.csv
  rm $1_tmp.csv
  sed -i '' 's@,\([0-9]\{2\}\)/\([0-9]\{2\}\)/\([0-9]\{2\}\)@,20\3-\2-\1@g' $1.csv
  sed -i '' 's/\//-/g' $1.csv
  sed -i '' 's/Date/Kickoff/g' $1.csv
  sed -i '' 's/HS/HOS/g' $1.csv
  sed -i '' 's/AS/AWS/g' $1.csv
  sed -i '' "s/'g/g/g" $1.csv
  sed -i '' "s/'D/D/g" $1.csv
  sed -i '' "s/'s/s/g" $1.csv
  sed -i '' "s/'m/m/g" $1.csv
# Addhoc fixes for bad CSV files
# fix I1
  if [ "$1" == "I1" ]; then
    sed -i '' "s/,,,,/,0,3,A,/" $1.csv
    sed -i '' "s/5,,5/5,0,5/" $1.csv
    sed -i '' "s/A,,,,,,,,,,,,,/A,0,0,0,0,0,0,0,0,0,0,0,0,/" $1.csv
  fi
# fix E3
  if [ "$1" == "E3" ]; then
    sed -i '' "s/,,,/,0,0,/" $1.csv
	sed -i '' "s/3,,/3,0,/" $1.csv
  fi
# fix 2016 F1
  if [ "$1" == "F1" ]; then
    sed -i '' "s/,,,,,,,,,,,,,,,,/,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,/" $1.csv
  fi
# fix 2017 I1 SP2
  if [ "$1" == "SP2" ] || [ "$1" == "I2" ]; then
    if [  ${PWD##*/} == "2017" ]; then
      sed -i '' 's/H,,,/H,0,0,0/' $1.csv
      sed -i '' 's/,,,/,0,0,/' $1.csv
    fi
  fi
# fix G1
  if [ "$1" == "G1" ]; then
    if [  ${PWD##*/} == "2015" ] || [  ${PWD##*/} == "2014" ]; then
      sed -i '' 's/0,3,A,,,,/0,3,A,0,3,A,/' $1.csv
      sed -i '' 's/3,0,H,,,,/3,0,H,3,0,H,/' $1.csv
      sed -i '' 's/Niki Volos,OFI,,,,,,,/Niki Volos,OFI,0,0,D,0,0,D,/' $1.csv
    fi
  fi
# fix T1
  if [ "$1" == "T1" ]; then
    if [  ${PWD##*/} == "2013" ]; then
      sed -i '' 's/0,3,A,,,,/0,3,A,0,3,A,/' $1.csv
    fi
  fi
# fix remove todays fixtures (they're not results)
  sed -i '' "/$(date +%Y-%m-%d)/d" $1.csv 
}
function create_teamlist {
tail -n +2 $1.csv | awk -F ',' '{print $3","$1}'| sed 's/ ,/,/g' | sort | uniq >> $PWDIR/data/teams_$2
}
function clean_tables {
TEMPLATE1="Select Divn,Kickoff as KO,HomeTeam as H_Team,AwayTeam as A_Team,FTHG as F,FTAG as A,FTR as R,HTHG as HF_F, HTAG as HF_A,HTR as HF_R,HOS as H_S,AWS as A_S,HOST as H_T, AWST as A_T,HF,AF,HC,AC,HY,AY,HR,AR from "
TEMPLATE2="Select Divn,Kickoff as KO,HomeTeam as H_Team,AwayTeam as A_Team,FTHG as F,FTAG as A,FTR as R,HTHG as HF_F, HTAG as HF_A,HTR as HF_R,0 as H_S,0 as A_S,0 as H_T, 0 as A_T,0 as HF,0 as AF,0 as HC,0 as AC,0 as HY,0 as AY,0 as HR,0 as AR from "
TEMPLATE3="Select Divn,Kickoff as KO,HomeTeam as H_Team,AwayTeam as A_Team,FTHG as F,FTAG as A,FTR as R,HTHG as HF_F, HTAG as HF_A,HTR as HF_R,0 as H_S,0 as A_S,0 as H_T,0 as A_T,0 as HF,0 as AF,0 as HC,0 as AC,HY,AY,HR,AR from "
TEMPLATE=$TEMPLATE1
  case $1 in
	1) TEMPLATE=$TEMPLATE1
	;;
	2) TEMPLATE=$TEMPLATE2
	;;
	3) TEMPLATE=$TEMPLATE3
	;;
 esac
 mysql -u$USER $DB -e "DROP TABLE IF EXISTS $2_$3"
 mysql -u$USER $DB -e "create table $2_$3 $TEMPLATE TMP_$3_$2"
 mysql -u$USER $DB -e "DROP TABLE IF EXISTS TMP_$3_$2"
}
function create_full_views {
echo "create historical tables for single leagues"
for A in B G N P T
  do
    NAME=$A"_ALL"
    mysql -u$USER $DB -e "DROP VIEW IF EXISTS \`$NAME\`"
    mysql -u$USER $DB -e "
    create view \`$NAME\` as
    select * from \`$A"1_"$LST3_SEASON\` UNION
    select * from \`$A"1_"$LST2_SEASON\` UNION
    select * from \`$A"1_"$LST1_SEASON\` UNION
    select * from \`$A"1_"$LAST_SEASON\` UNION
    select * from \`$A"1_"$CURR_SEASON\`"
  done
echo "create historical tables for two leagues"
for A in D F I SP
  do
    NAME=$A"_ALL"
    mysql -u$USER $DB -e "DROP VIEW IF EXISTS \`$NAME\`"
    mysql -u$USER $DB -e "
    create view \`$NAME\` as
    select * from \`$A"1_"$LST3_SEASON\` UNION
    select * from \`$A"2_"$LST3_SEASON\` UNION
    select * from \`$A"1_"$LST2_SEASON\` UNION
    select * from \`$A"2_"$LST2_SEASON\` UNION
    select * from \`$A"1_"$LST1_SEASON\` UNION
    select * from \`$A"2_"$LST1_SEASON\` UNION
    select * from \`$A"1_"$LAST_SEASON\` UNION
    select * from \`$A"2_"$LAST_SEASON\` UNION
    select * from \`$A"1_"$CURR_SEASON\` UNION
    select * from \`$A"2_"$CURR_SEASON\`"
  done
echo "create historical tables for four leagues"
for A in SC
  do
    NAME=$A"_ALL"
    mysql -u$USER $DB -e "DROP VIEW IF EXISTS \`$NAME\`"
    mysql -u$USER $DB -e "
    create view \`$NAME\` as
    select * from \`$A"0_"$LST3_SEASON\` UNION
    select * from \`$A"1_"$LST3_SEASON\` UNION
    select * from \`$A"2_"$LST3_SEASON\` UNION
    select * from \`$A"3_"$LST3_SEASON\` UNION
    select * from \`$A"0_"$LST2_SEASON\` UNION
    select * from \`$A"1_"$LST2_SEASON\` UNION
    select * from \`$A"2_"$LST2_SEASON\` UNION
    select * from \`$A"3_"$LST2_SEASON\` UNION
    select * from \`$A"0_"$LST1_SEASON\` UNION
    select * from \`$A"1_"$LST1_SEASON\` UNION
    select * from \`$A"2_"$LST1_SEASON\` UNION
    select * from \`$A"3_"$LST1_SEASON\` UNION
    select * from \`$A"0_"$LAST_SEASON\` UNION
    select * from \`$A"1_"$LAST_SEASON\` UNION
    select * from \`$A"2_"$LAST_SEASON\` UNION
    select * from \`$A"3_"$LAST_SEASON\` UNION
    select * from \`$A"0_"$CURR_SEASON\` UNION
    select * from \`$A"1_"$CURR_SEASON\` UNION
    select * from \`$A"2_"$CURR_SEASON\` UNION
    select * from \`$A"3_"$CURR_SEASON\`"
  done
echo "create historical tables for five leagues"
for A in E
  do
    NAME=$A"_ALL"
    mysql -u$USER $DB -e "DROP VIEW IF EXISTS \`$NAME\`"
    mysql -u$USER $DB -e "
    create view \`$NAME\` as
    select * from \`$A"0_"$LST3_SEASON\` UNION
    select * from \`$A"1_"$LST3_SEASON\` UNION
    select * from \`$A"2_"$LST3_SEASON\` UNION
    select * from \`$A"3_"$LST3_SEASON\` UNION
    select * from \`$A"C_"$LST3_SEASON\` UNION
    select * from \`$A"0_"$LST2_SEASON\` UNION
    select * from \`$A"1_"$LST2_SEASON\` UNION
    select * from \`$A"2_"$LST2_SEASON\` UNION
    select * from \`$A"3_"$LST2_SEASON\` UNION
    select * from \`$A"C_"$LST2_SEASON\` UNION
    select * from \`$A"0_"$LST1_SEASON\` UNION
    select * from \`$A"1_"$LST1_SEASON\` UNION
    select * from \`$A"2_"$LST1_SEASON\` UNION
    select * from \`$A"3_"$LST1_SEASON\` UNION
    select * from \`$A"C_"$LST1_SEASON\` UNION
    select * from \`$A"0_"$LAST_SEASON\` UNION
    select * from \`$A"1_"$LAST_SEASON\` UNION
    select * from \`$A"2_"$LAST_SEASON\` UNION
    select * from \`$A"3_"$LAST_SEASON\` UNION
    select * from \`$A"C_"$LAST_SEASON\` UNION
    select * from \`$A"0_"$CURR_SEASON\` UNION
    select * from \`$A"1_"$CURR_SEASON\` UNION
    select * from \`$A"2_"$CURR_SEASON\` UNION
    select * from \`$A"3_"$CURR_SEASON\` UNION
    select * from \`$A"C_"$CURR_SEASON\`"
  done
}
function all_teams {
cd $PWDIR/data/
echo "team,yr5,lg5,yr4,lg4,yr3,lg3,yr2,lg2,yr1,lg1" > teams
echo "season,league,year" > legend
for a in {1..5}; do printf yr${a}","; printf lg${a}","; printf $(($NEXT_SEASON -${a}))"\n";done >> legend
cat teams_* | cut -d',' -f1 | sort | uniq | while read line
do
  TABL=""
  printf "$line" >> teams
  for A in $LST3_SEASON $LST2_SEASON $LST1_SEASON $LAST_SEASON $CURR_SEASON
    do
        TMP="teams_"$A
        DN=$(cat $TMP | egrep ^"$line," | cut -d',' -f2)
        if [ "$DN" == "" ]; then DN="NA"; fi
	if [ "$DN" != "NA" ]; then TABL=$(echo $DN | rev | cut -c 2- | rev)"_ALL"; fi
        printf ",$A,$DN" >> teams
    done
    printf "\n" >> teams
    mysql -u$USER $DBT -e "create view \`$line\` as select * from $DB.$TABL where H_Team = \"$line\" or A_Team = \"$line\""
    printf "."
done
  printf "\n"
  WDIR=$(pwd)
  create_table teams teams
  mysql -u$USER $DB -e "DROP TABLE IF EXISTS teams"
  mysql -u$USER $DB < teams.sql
  upload_csv teams teams
  mysql -u$USER $DB -e "ALTER TABLE teams ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY"
  #legend added
  create_table legend legend
  mysql -u$USER $DB -e "DROP TABLE IF EXISTS legend"
  mysql -u$USER $DB < legend.sql
  upload_csv legend legend
  mysql -u$USER $DB -e "ALTER TABLE legend ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY"
  rm teams_*
  rm teams.sql
  rm legend
  rm legend.sql
}
function create_stats {
cd $PWDIR
if [ "$1" == "" ]; then TYPE="L"; else TYPE=$1; fi
if [ "$2" == "" ]; then
  TBNAME=$CURR_SEASON"_league_table"; COL="lg1"; YEAR=$CURR_SEASON; TD=$(date +%Y-%m-%d)
else
  TBNAME=$2; COL=$3; YEAR=$4; TD=$5
fi
case $1 in
  L|F) QUERY="league_query"
  ;;
  LS) QUERY="league_form_query"
  ;;
  P) QUERY="all_play_query"
  ;;
  PF) QUERY="ha_play_query";TYPE="PF"
  ;;
  *) QUERY="league_query"
  ;;
esac

if [ $TYPE == "P" ]; then
  CRTBL="create table $TBNAME (Dvn varchar(10),Team varchar(35),Games int,Shots int,Shots_t int,Goals_f decimal(4,2),Shots_a int,Shots_at int,Goals_a decimal(4,2),pc_shots_t int,pc_goals_t  int)"
fi

if [ $TYPE == "PF" ]; then
  CRTBL="create table $TBNAME (Divn varchar(10),Team varchar(35),H_Games int,H_S decimal(4,2),H_ST decimal(4,2),H_G decimal(4,2),H_SA decimal(4,2),H_STA decimal(4,2),H_GA decimal(4,2),A_Games int,A_S decimal(4,2),A_ST decimal(4,2),A_G decimal(4,2),A_SA decimal(4,2),A_STA decimal(4,2),A_GA decimal(4,2))"
fi

if [ $TYPE == "L" ] || [ $TYPE == "F" ]; then
  CRTBL="create table $TBNAME (Dvn varchar(10),Team varchar(35),H_P int,H_W int,H_D int,H_L int,H_F int,H_A int,HGD int,HPS int,A_P int,A_W int,A_D int,A_L int,A_F int,A_A int,AGD int,APS int,GD int,PTS int, Pos int)"
fi
if [ $TYPE == "LS" ]; then
  CRTBL="create table $TBNAME (Dvn varchar(10),Team varchar(35),H_P int,H_W int,H_D int,H_L int,H_F int,H_A int,HGD int,HPS int,Hpos int,A_P int,A_W int,A_D int,A_L int,A_F int,A_A int,AGD int,APS int, APos int)"
fi
mysql -u$USER $DBL -e "DROP TABLE IF EXISTS $TBNAME"
mysql -u$USER $DBL -e "$CRTBL"
mysql -u$USER $DB -e "select team,$COL,id from teams where $COL !=\"NA\"" | sed 1d | awk -F"\t" '{print $1":"$2":"$3}'| while read line
  do
    DUD=0
    TM=$(echo $line | cut -d':' -f1); LG=$(echo $line | cut -d':' -f2); CT=$(echo $line | cut -d':' -f3)
    SD=$YEAR"-"$(mysql -u$USER $DB -e "select starts from competitions where CID=\"$LG\"" | sed 1d)
    #if [ "$TYPE" == "F" ] || [ "$TYPE" == "PF" ]; then
    if [ "$TYPE" == "F" ]; then
      LAST=$(mysql -u$USER $DBT -e "select * from \`$TM\` where KO between '$SD' and '$TD' order by KO desc limit 6" | sed 1d | wc -l)
      if [ $LAST -gt 0 ]; then
        SD=$(mysql -u$USER $DBT -e "select * from \`$TM\` where KO between '$SD' and '$TD' order by KO desc limit 6" | tail -1 | awk '{print $2}')
      else
        DUD=1
      fi
    fi
      if [ $DUD -eq 0 ]; then
        cat data/query/$QUERY | sed "s/TEAMNAME/$TM/g" | sed "s/YYYY-MM-DD/$SD/g" | sed "s/YYYY-MM-TT/$TD/g" | sed "s/SQLCOMM/INSERT INTO $TBNAME/g" |  mysql -u$USER $DBL
      else
        if [ $TYPE == "P" ];then
          UPDTBL="insert into $TBNAME (Dvn,Team,Games,Shots,Shots_t,Goals_f,Shots_a,Shots_at,Goals_a,pc_Shots_t,pc_Goals_t) values ('$LG','$TM',0,0,0,0,0,0,0,0,0,0,0)"
        fi
        if [ $TYPE == "PF" ]; then
	  UPDTBL="insert into $TBNAME (Divn,Team,H_Games,H_S,H_ST,H_G,H_SA,H_STA,H_GA,A_Games,A_S,A_ST,A_G,A_SA,A_STA,A_GA) values ('$LG','$TM',0,0,0,0,0,0,0,0,0,0,0,0,0,0)"
        fi
        if [ $TYPE == "L" ] || [ $TYPE == "F" ]; then
          UPDTBL="insert into $TBNAME (Dvn,Team,HPlayed,HWon,HDrawn,HLost,HFor,HAgainst,HGD,HPts,APlayed,AWon,ADrawn,ALost,AFor,AAgainst,AGD,APts,Pts) values ('$LG','$TM',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)"
        fi
	if [ $TYPE ==  "LS" ]; then
          UPDTBL="insert into $TBNAME (Dvn,Team,H_P,H_W,H_D,H_L,H_F,H_A,HGD,HPS,HPos,A_P,A_W,A_D,A_L,A_F,A_A,AGD,APS,APos) values ('$LG','$TM',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)"
        fi
      mysql -u$USER $DBL -e "$UPDTBL"
      fi
    printf "."
  done
  printf "\n"
}
function add_league_position {
if [ "$1" == "" ]; then TABLE=$CURR_SEASON"_league_table"; else TABLE=$1; fi
if [ "$2" != "" ]; then
  POS=$2;GD=$3;PNS=$4
else
  POS="Pos";GD="(HGD+AGD)";PNS="PTS"
fi
sed 1d $PWDIR/data/competitions | while read line
  do
    LG=$(echo $line | cut -d',' -f1)
    QURY="select Dvn,Team,$PNS,$POS from (select Dvn,Team,$GD as GD,$PNS,@i:=@i+1 $POS from (Select @i:=0) as i,$TABLE where Dvn=\"$LG\" order by $PNS desc, $GD desc) as Bill"
    mysql -u$USER $DBL -N -B -e "$QURY" | awk -F "\t" '{print $1","$2,","$3","$4}' | sed 's/ ,/,/g' | while read line
    do
      TM=$(echo $line | cut -d',' -f2)
      PS=$(echo $line | cut -d',' -f4)
      mysql -u$USER $DBL -e "UPDATE $TABLE SET $POS=\"$PS\" WHERE Dvn=\"$LG\" AND Team=\"$TM\""
    done
  done
}
function perform_stats {
cd $PWDIR
if [ "$1" == "" ]; then
  TBNAME=$CURR_SEASON"_perform_table"; LGT=$CURR_SEASON"_league_table";COL="lg1"; YEAR=$CURR_SEASON; TD=$(date +%Y-%m-%d)
else
  TBNAME=$1; COL=$2; YEAR=$3; TD=$4; LGT=$5 #COL is the league column for the year in question
fi
mysql -u$USER $DBL -e "DROP TABLE IF EXISTS $TBNAME"
mysql -u$USER $DBL -e "create table $TBNAME (Dvn varchar(10),Team varchar(35), hwt int, hwm int, hwb int,hdt int,hdm int,hdb int,hlt int,hlm int,hlb int,awt int, awm int, awb int,adt int,adm int,adb int,alt int,alm int,alb int)"
mysql -u$USER $DB -e "select team,$COL,id from teams where $COL !=\"NA\"" | sed 1d | awk -F"\t" '{print $1":"$2":"$3}'| while read line
  do
    TM=$(echo $line | cut -d':' -f1); LG=$(echo $line | cut -d':' -f2); CT=$(echo $line | cut -d':' -f3)
    SD=$YEAR"-"$(mysql -u$USER $DB -e "select starts from competitions where CID=\"$LG\"" | sed 1d)
    MB=$(mysql -u$USER $DB -e "select Members from competitions where CID=\"$LG\"" | sed 1d)
    TOP=$(($MB/3));MID=$(($TOP+$TOP))
    cat data/query/perform_query | sed "s/DIVN/$LG/g" | sed "s/TEAMNAME/$TM/g" | sed "s/LEAGUE_TABLE/$LGT/g" | sed "s/YYYY-MM-DD/$SD/g" | sed "s/YYYY-MM-TT/$TD/g" | sed "s/TOP/$TOP/g" | sed "s/MID/$MID/g" | sed "s/SQLCOMM/INSERT INTO Leagues.$TBNAME/g" | mysql -u$USER $DBT -N
  done
}
function import_results {
cd /$PWDIR/data
echo "import results from $1"
sed 1d $PWDIR/data/competitions | while read line
  do
    RES=$(echo $line | cut -d',' -f1)
    TYP=$(echo $line | cut -d',' -f8)
    cd $PWDIR/data/seasons/$1
    clean_csv $RES
    upload_fixtures $RES.csv $1
    clean_tables $TYP $RES $1
    create_teamlist $RES $1
  done
}
function weight_table {
mysql -u$USER $DBL -e "DROP TABLE IF EXISTS $1"
$PWDIR/osx_weight_table.py $1
}
function run_table {
mysql -u$USER $DBL -e "DROP TABLE IF EXISTS $1"
$PWDIR/osx_run_table.py $1
}
function mega_perform {
TBNAME=$CURR_SEASON"_mega_perform"
mysql -u$USER $DBL -e "DROP TABLE IF EXISTS $TBNAME"
mysql -u$USER $DBL -e "create table $TBNAME (Dvn varchar(10),Team varchar(35), hpt float(4,2), hpm float(4,2), hpb float(4,2),apt float(4,2),apm float(4,2),apb float(4,2))"
mysql -u$USER $DB -e "select team from teams where lg1 !=\"NA\"" | sed 1d | while read TM
  do
    cat data/query/mega_perform_query | sed "s/TEAMNAME/$TM/g" | sed "s/LAST_YEAR/$LAST_SEASON/g" | sed "s/CURR_YEAR/$CURR_SEASON/g" | sed "s/SQLCOMM/INSERT INTO Leagues.$TBNAME/g" | mysql -u$USER $DBL -N
  done
}
function history {
  if [ $1 -lt $CURR_SEASON ]; then 
    EOD=$(($1 + 1))-07-07
    LG=$(mysql -u$USER $DB -e "select league from legend where year=$1" | tail -1)
    echo "create history"
    create_stats L $1_league_table $LG $1 $EOD
    add_league_position $1_league_table
    perform_stats $1_perform_table $LG $1 $EOD $1_league_table
    create_stats P $1_play_table $LG $1 $EOD
    #create_stats PF $1_ha_play_table $LG $1 $(date +%Y-%m-%d)
  fi
}
while getopts :uih flag
  do
    case $flag in
      u)UPD=1;;
      i)INT=1;;
      h)HST=1;;
      *);;
    esac
  done
shift $(($OPTIND -1))

# download
if [ $INT == 1 ]; then
  pull_data
  # Create databases;
  echo "Create Databases"
  create_db $DB
  create_db $DBT
  create_db $DBL
  create_db $DBP
  echo "Create mysql accounts"
  create_db_accounts
  # Create competition table;
  echo "Create Competition Data"
  cd $PWDIR/data
  create_competition "competitions"
  # Import results to MySQL
  echo "Import Results"
  import_results $CURR_SEASON
  import_results $LAST_SEASON
  import_results $LST1_SEASON
  import_results $LST2_SEASON
  import_results $LST3_SEASON
fi
if [ $UPD == 1 ]; then
  download_league $CURR_SEASON
  import_results $CURR_SEASON
fi
if [ $UPD == 1 ] || [ $INT == 1 ];then
  #create the views
  echo "create full views"
  create_full_views
fi
#create teams table
if [ $INT == 1 ];then
  echo "create team stat views"
  all_teams
fi
if [ $UPD == 1 ] || [ $INT == 1 ];then
  echo "create league & form tables"
  create_stats
  add_league_position
  TMPTBL=$CURR_SEASON"_form_table"
  create_stats F $TMPTBL lg1 $CURR_SEASON $(date +%Y-%m-%d)
  echo "add form position"
  add_league_position $TMPTBL
  echo "create last six home away"
  TMPTBL=$CURR_SEASON"_league_form_table"
  create_stats LS $TMPTBL lg1 $CURR_SEASON $(date +%Y-%m-%d)
  echo "add last 6 form position"
  add_league_position $TMPTBL "HPos" "HGD" "HPS"
  add_league_position $TMPTBL "APos" "AGD" "APS"
  echo "create goal form tables"
  TMPTBL=$CURR_SEASON"_play_table"
  create_stats P $TMPTBL lg1 $CURR_SEASON $(date +%Y-%m-%d)
  echo "create performance tables"
  perform_stats
  echo "create weight table"
  TMPTBL=$CURR_SEASON"_weight_table"
  weight_table $TMPTBL
  history $LAST_SEASON
  echo "create mega perform table"
  mega_perform
  echo "create ha_play table"
  TMPTBL=$CURR_SEASON"_ha_play_table"
  create_stats PF $TMPTBL lg1 $LAST_SEASON $(date +%Y-%m-%d)
  TMPTBL=$CURR_SEASON"_run_table"
  echo "create run table"
  run_table $TMPTBL
fi
if [ $HST == 1 ]; then
  history $1
fi
#create_stats PF 2017_ha_play_table lg1 $LAST_SEASON $(date +%Y-%m-%d)
#create_stats PF $TMPTBL lg1 $LAST_SEASON $(date +%Y-%m-%d)
#mega_perform
#create_stats L 2016_league_table lg2 $LAST_SEASON 2017-07-01
#add_league_position 2016_league_table
#perform_stats
#perform_stats 2016_perform_table lg2 $LAST_SEASON 2017-07-01 2016_league_table
#TMPTBL=$CURR_SEASON"_form_table"
#create_stats F $TMPTBL lg1 $CURR_SEASON $(date +%Y-%m-%d)
#add_league_position $TMPTBL
#echo "create last six home away"
#TMPTBL=$CURR_SEASON"_league_form_table"
#create_stats LS $TMPTBL lg1 $CURR_SEASON $(date +%Y-%m-%d)
#add_league_position $TMPTBL "HPos" "HGD" "HPS"
#add_league_position $TMPTBL "APos" "AGD" "APS"
#echo "add league position"
#add_league_position
#add_league_position $TMPTBL
#create_stats L 2015_league_table lg2 $LAST_SEASON 2016-07-01
#create_stats F league_form_table lg1 2016 $(date +%Y-%m-%d)
#echo "create goal form tables"
#TMPTBL=$CURR_SEASON"_play_table"
#create_stats P $TMPTBL lg1 $CURR_SEASON $(date +%Y-%m-%d)
#create_stats PA away_play_table lg1 $CURR_SEASON $(date +%Y-%m-%d)
#create_stats PH home_play_table lg1 $CURR_SEASON $(date +%Y-%m-%d)
#echo "create performance tables"
#echo "create weight table"
#TMPTBL=$CURR_SEASON"_weight_table"
#weight_table $TMPTBL
