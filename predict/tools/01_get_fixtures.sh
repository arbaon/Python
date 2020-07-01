#!/bin/bash
USER="root"
PASS=""
DB="Predict"
DBT="predict"
DBV="predict_view"
#DBT="test"
DBO="predict_odds"
PWDIR=$(dirname `pwd`)
URL="www.football-data.co.uk/fixtures.csv"

function pull_fix {
  if [ -d "$PWDIR/data/fixtures" ]; then
    rm -rf $PWDIR/data/fixtures
  fi
	mkdir $PWDIR/data/fixtures
  cd $PWDIR/data/fixtures
  wget $URL
  # fix the date
  sed -i 's@/2018,@/18,@g' $1.csv
  sed -i 's@/2019,@/19,@g' $1.csv
  sed -i 's@,\([0-9]\{2\}\)/\([0-9]\{2\}\)/\([0-9]\{2\}\)@,20\3-\2-\1@g' $1.csv
  sed -i "s/'g/g/g" $1.csv
  sed -i "s/'D/D/g" $1.csv
  sed -i "s/'s/s/g" $1.csv
  sed -i "s/'m/m/g" $1.csv
  sed -i "s/'G/G/g" $1.csv
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
  sed -i "s/Date varchar(35)/Kickoff date/" $2.sql
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
mysql -u$USER $DB -e "alter table $2 drop column FTHG, drop column FTAG, drop column FTR,drop column HTHG,drop column HTAG,drop column HTR"
mysql -u$USER $DB -e "DROP TABLE IF EXISTS $DBO"
#mysql -u$USER $DB -e "create table $DBO (select Divn, Kickoff,HomeTeam,AwayTeam,if(B365D<3.3,\"D\",\"-\") as B365_D,if(B365H<B365A,if(BWH<B365D,\"H\",\"D\"),if(B365A<B365D,\"A\",\"D\")) as B365,if(BWD<3.3,\"D\",\"-\") as BW_D,if(BWH<BWA,if(BWH<BWD,\"H\",\"D\"),if(BWA<BWD,\"A\",\"D\")) as BW,if(IWD<=3.3,\"D\",\"-\") as IW_D,if(IWH<IWA,if(IWH<IWD,\"H\",\"D\"),if(IWA<IWD,\"A\",\"D\")) as IW,if(LBD<3.2,\"D\",\"-\") as LB_D,if(LBH<LBA,if(LBH<LBD,\"H\",\"D\"),if(LBA<LBD,\"A\",\"D\")) as LB,if(PSD<3.2,\"D\",\"-\") as PS_D,if(PSH<PSA,if(PSH<PSD,\"H\",\"D\"),if(PSA<PSD,\"A\",\"D\")) as PS,if(WHD<3.2,\"D\",\"-\") as WH_D,if(WHH<WHA,if(WHH<WHD,\"H\",\"D\"),if(WHA<WHD,\"A\",\"D\")) as WH,if(VCD<3.2,\"D\",\"-\") as VC_D,if(VCH<VCA,if(LBH<VCD,\"H\",\"D\"),if(VCA<VCD,\"A\",\"D\")) as VC,round((BWH+IWH+LBH+PSH+WHH+VCH)/6,2) as H,round((BWD+IWD+LBD+PSD+WHD+VCD)/6,2) as D,round((BWA+IWA+LBA+PSA+WHA+VCA)/7,2) as A from $2)"
mysql -u$USER $DB -e "create table $DBO (select Divn, Kickoff,HomeTeam,AwayTeam,if(B365D<3.3,\"D\",\"-\") as B365_D,if(B365H<B365A,if(BWH<B365D,\"H\",\"D\"),if(B365A<B365D,\"A\",\"D\")) as B365,if(BWD<3.3,\"D\",\"-\") as BW_D,if(BWH<BWA,if(BWH<BWD,\"H\",\"D\"),if(BWA<BWD,\"A\",\"D\")) as BW,if(IWD<=3.3,\"D\",\"-\") as IW_D,if(IWH<IWA,if(IWH<IWD,\"H\",\"D\"),if(IWA<IWD,\"A\",\"D\")) as IW,if(PSD<3.2,\"D\",\"-\") as PS_D,if(PSH<PSA,if(PSH<PSD,\"H\",\"D\"),if(PSA<PSD,\"A\",\"D\")) as PS,if(WHD<3.2,\"D\",\"-\") as WH_D,if(WHH<WHA,if(WHH<WHD,\"H\",\"D\"),if(WHA<WHD,\"A\",\"D\")) as WH,if(VCD<3.2,\"D\",\"-\") as VC_D,if(VCH<VCA,if(VCH<VCD,\"H\",\"D\"),if(VCA<VCD,\"A\",\"D\")) as VC,round((BWH+IWH+B365H+PSH+WHH+VCH)/6,2) as H,round((BWD+IWD+B365D+PSD+WHD+VCD)/6,2) as D,round((BWA+IWA+B365A+PSA+WHA+VCA)/7,2) as A from $2)"
mysql -u$USER $DB -e "drop table $2"
}
function create_fix_table {
mysql -u$USER $DB -e "DROP TABLE IF EXISTS $DBT"
mysql -u$USER $DB -e "create table $DBT (id int not null auto_increment,dvn varchar(10), KO date,h_team varchar(35), a_team varchar(35),lp int, fp int, lpf int, fpf int, wa int, wha int, fib int, gls int, alg int,tot int,goalpw double,totpw double,primary key (id))"
}

function upload_csv {
cp $1 /tmp/
mysql -u$USER $DB -e "LOAD DATA INFILE \"/tmp/$1\" INTO TABLE $2 COLUMNS TERMINATED BY \",\" IGNORE 1 LINES"
rm /tmp/$1
}
function create_view {
mysql -u$USER $DB -e "DROP VIEW IF EXISTS $DBV"
mysql -u$USER $DB -e "create view $DBV as select $DBT.*,$DBO.H,$DBO.D,$DBO.A from $DBT left join $DBO on $DBT.h_team = $DBO.HomeTeam"
}

#create_db
create_fix_table
pull_fix fixtures
cd $PWDIR/data/fixtures
create_table fixtures.csv predict
export_tmp_table predict tmp_predict
create_view
