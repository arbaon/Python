#!/bin/bash
CURR_SEASON="2017"
USER="root"
PASS=""
DBP="Predict"
DBT="Predict_"$CURR_SEASON
PWDIR=$(pwd ../)
function create_db {
mysql -u$USER -e "DROP DATABASE IF EXISTS $DBP"
mysql -u$USER -e "create database $DBP"
}

function create_table {
mysql -u$USER $DBP -e "DROP TABLE IF EXISTS $DBT"
mysql -u$USER $DBP -e "create table $DBT (dvn varchar(10), KO date,h_team varchar(35), a_team varchar(35),lp int, fp int, lpf int, fpf int, wa int, wha int, fib int, gls int, tot int)"
}
create_db
create_table
