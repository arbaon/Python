#!/usr/bin/python
import MySQLdb
import sys
from sequence import Sequence
def run_query(query,DTB,type):
    if type !="U":
        type = "Q"
    db=MySQLdb.connect(user="python", passwd="Python8177!", db=DTB)
    cur=db.cursor()
    cur.execute(query)
    if type == "Q":
        data=cur.fetchall()
    else:
	db.commit()
    cur.close
    db.close
    if type == "Q":
        return data
def test_table_exists(tablename,TDB):
    query='SELECT * FROM information_schema.tables where table_name="%s"' % tablename
    test=run_query(query,TDB,"Q")
    for row in test:
	if row:
	    return 1
	else:
	    return 0   
def generate_sequence(team,ttype):
    findteam=test_table_exists(team,"Teams")
    if findteam == 1:
	if ttype == "H":
            query="""select Points,GD from (select KO,if(if(H_Team="%s",F-A,A-F) > 0,if(H_Team ="%s",3,4),if(R="D",if(H_Team="%s",1,2),0)) as Points,if(H_Team="%s",F-A,A-F) as GD from `%s` where H_Team ="%s"order by KO desc limit 6) sub order by KO asc""" % (team,team,team,team,team,team)
	elif ttype == "A":
	    query="""select Points,GD from (select KO,if(if(H_Team="%s",F-A,A-F) > 0,if(H_Team ="%s",3,4),if(R="D",if(H_Team="%s",1,2),0)) as Points,if(H_Team="%s",F-A,A-F) as GD from `%s` where H_Team !="%s" order by KO desc limit 6) sub order by KO asc""" % (team,team,team,team,team,team)
	else:
	    query="""select Points,GD from (select KO,if(if(H_Team="%s",F-A,A-F) > 0,if(H_Team ="%s",3,4),if(R="D",if(H_Team="%s",1,2),0)) as Points,if(H_Team="%s",F-A,A-F) as GD from `%s` order by KO desc limit 6) sub order by KO asc""" % (team,team,team,team,team)
        results = run_query(query,"Teams","Q")
        X=Sequence()
        Y=[]
        for row in results:
            X.runseq([row[0],row[1]])
        Y=X.get_weights()
	return Y
    else:
	print "VOID"
def run_all(FILENAME):
    tquery ="create table %s (Dvn varchar(10),team varchar(35),pl int,pts decimal(4,2),acc decimal(4,2),gbon decimal(4,2),bon int,hpl int,hpts decimal(4,2),hacc decimal(4,2),hgbon decimal(4,2),hbon int,apl int,apts decimal(4,2),aacc decimal(4,2),agbon decimal(4,2),abon int)" %(FILENAME)
    run_query(tquery,"Leagues","U")
    query='select Team,lg1 from teams where lg1 !="NA"'
    teams = run_query(query,"Results","Q")
    for row in teams:
	A=generate_sequence(row[0],"H")
	B=generate_sequence(row[0],"A")
	C=generate_sequence(row[0],"F")
	query="insert into %s (Dvn,team,pl,pts,acc,gbon,bon,hpl,hpts,hacc,hgbon,hbon,apl,apts,aacc,agbon,abon) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (FILENAME,row[1],row[0],C[5],C[0],C[2],round(C[3],2),C[4],A[5],A[0],A[2],round(A[3],2),A[4],B[5],B[0],B[2],round(B[3],2),B[4])
	run_query(query,"Leagues","U")
total = len(sys.argv) 
if total > 1:
    FILENAME=str(sys.argv[1])
else:
    FILENAME="recent_form"
run_all(FILENAME)
