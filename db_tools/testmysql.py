#!/usr/bin/python
import MySQLdb
import csv
import subprocess
def create_db( league ):
    db=MySQLdb.connect(user="root")
    query="DROP DATABASE IF EXISTS "+league+";CREATE DATABASE "+league
    print (query)
    cur=db.cursor()
    cur.execute(query,)
    cur.close()
    db.close()
def create_tb( mytb, mydb, filename ):
    db=MySQLdb.connect(user="root", db=mydb);
    SQL="CREATE TABLE "+mytb+" ( Kickoff date, HomeTeam varchar(20), AwayTeam varchar(20), FTHG int, FTAG int, FTR varchar(2), HTHG int, HTAG int, HTR varchar(2), Referee varchar(20), HOS int, AWS int, HST int, AST int, HF int, AF int, HC int, AC int, HY int, AY int, HR int, AR int )"
    print(SQL)
    curs=db.cursor()
    curs.execute(SQL)
    #for data in curs.fetchall():
        #print '%s\t' % data
    #curs.close()
    csv_data =csv.reader(file(filename))
    headers=csv_data.next()
    for row in csv_data:
	query="INSERT INTO %s (Kickoff,HomeTeam,AwayTeam,FTHG,FTAG,FTR,HTHG,HTAG,HTR,Referee,HOS,AWS,HST,AST,HF,AF,HC,AC,HY,AY,HR,AR) VALUES (STR_TO_DATE('%s','%%d/%%m/%%y'),'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' )" % (mytb, row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22])
	curs.execute(query)
	db.commit()
	print(query)
    curs.close()
    db.close
create_db( 'premier' )
create_tb( 'results','premier','E0.csv')
