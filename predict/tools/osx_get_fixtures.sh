#!/bin/bash
USER="root"
PASS=""
DB="Predict"
DBT="predict"
PWDIR=$(pwd ../)
URL="www.football-data.co.uk/fixtures.csv"

function pull_fix {
  if [ -d "$PWDIR/data/fixtures" ]; then
    rm -rf $PWDIR/data/fixtures
  fi
	mkdir $PWDIR/data/fixtures
  cd $PWDIR/data/fixtures
  wget $URL
  # fix the date
  sed -i '' 's@,\([0-9]\{2\}\)/\([0-9]\{2\}\)/\([0-9]\{2\}\)@,20\3-\2-\1@g' $1.csv
  sed -i '' "s/'g/g/g" $1.csv
  sed -i '' "s/'D/D/g" $1.csv
  sed -i '' "s/'s/s/g" $1.csv
  sed -i '' "s/'m/m/g" $1.csv
  sed -i '' "s/'G/G/g" $1.csv
  cd $PWDIR
}

function create_db {
mysql -u$USER -e "DROP DATABASE IF EXISTS $DB"
mysql -u$USER -e "create database $DB"
}

function create_table_import {
  printf "create table $2( " > $2.sql
  head -1 $1 | sed -e 's/Div/Divn/g' | sed -e 's/>2.5/gt25/g' | sed -e 's/<2.5/lt25/g' | sed -e 's/,/ varchar(35),/g' >> $2.sql
  printf " varchar(35));" >> $2.sql
  sed -i '' "s/Date varchar(35)/Kickoff date/" $2.sql
}

function create_table {
  #table name, file name
  create_table_import $1 tmp_$2
  mysql -u$USER $DB -e "DROP TABLE IF EXISTS tmp_$2"
  mysql -u$USER $DB < tmp_$2.sql
  upload_csv $1 tmp_$2
  rm tmp_$2.sql
}
function export_tmp_table {
mysql -u$USER $DB -e "insert into $1 (dvn,KO,h_team,a_team) select divn,kickoff,hometeam,awayteam from $2"
mysql -u$USER $DB -e "drop table $2"
}
function create_fix_table {
mysql -u$USER $DB -e "DROP TABLE IF EXISTS $DBT"
mysql -u$USER $DB -e "create table $DBT (id int not null auto_increment,dvn varchar(10), KO date,h_team varchar(35), a_team varchar(35),lp int, fp int, lpf int, fpf int, wa int, wha int, fib int, gls int, tot int,result varchar(5),primary key (id))"
}

function upload_csv {
cp $1 /tmp/
mysql -u$USER $DB -e "LOAD DATA INFILE \"/tmp/$1\" INTO TABLE $2 COLUMNS TERMINATED BY \",\" IGNORE 1 LINES"
rm /tmp/$1
}

create_db
create_fix_table
pull_fix fixtures
cd $PWDIR/data/fixtures
create_table fixtures.csv predict
export_tmp_table predict tmp_predict
