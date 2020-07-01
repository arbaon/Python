#!/usr/local/bin/python
import MySQLdb
import sys
def run_query(DTB,query,type):
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
def season_run(league,team):
    query="""select if(R="L",0,1) as RT from (select if( R="D","D",if(H_team="%s",if(R="H","W","L"),if(R="A","W","L"))) as R from `%s` order by KO desc limit 40) as RES"""% (team,team)
    results=run_query(league,query,"Q")
    rval=[]
    acount=0
    scount=0
    bestrun=0
    newrun=0
    lrow=0
    for row in results:
        if row[0] == 0:
            scount=scount+1
	    if newrun > bestrun:
		bestrun=newrun
		newrun=0
        else:
	    newrun=newrun+1
            if lrow == 0:
                scount=scount+1
        lrow = row[0]
	acount=acount+1
    perct=round(100-(float(scount) / float(acount) * 100),2)
    rval.insert(0,perct)
    if newrun > bestrun:
	bestrun=newrun
    rval.insert(1,bestrun)
    return rval
       
def season_run_home(league,team):
    query="""select if(R="L",0,1) as RS from (select if(R="H","W",if(R="D","D","L")) as R from `%s` where H_Team = "%s" order by KO desc limit 20 ) as RES""" % (team,team)
    results=run_query(league,query,"Q")
    rval=[]
    scount=0
    bestrun=0
    newrun=0
    acount=0
    lrow=0
    for row in results:
        if row[0] == 0:
            scount=scount+1
	    if newrun > bestrun:
		bestrun=newrun
		newrun=0
        else:
	    newrun=newrun+1
            if lrow == 0:
                scount=scount+1
        lrow = row[0]
	acount=acount+1
    perct=100-(float(scount) / float(acount) * 100)
    rval.insert(0,perct)
    if newrun > bestrun:
	bestrun=newrun
    rval.insert(1,bestrun)
    return rval

def season_run_away(league,team):
    query="""select if(R="L",0,1) as RS from (select if(R="A","W",if(R="D","D","L")) as R from `%s` where A_Team = "%s" order by KO desc limit 20 ) as RES""" % (team,team)
    results=run_query(league,query,"Q")
    rval=[]
    scount=0
    bestrun=0
    newrun=0
    acount=0
    lrow=0
    for row in results:
        if row[0] == 0:
            scount=scount+1
	    if newrun > bestrun:
		bestrun=newrun
		newrun=0
        else:
	    newrun=newrun+1
            if lrow == 0:
                scount=scount+1
        lrow = row[0]
	acount=acount+1
    perct=100-(float(scount) / float(acount) * 100)
    rval.insert(0,perct)
    if newrun > bestrun:
	bestrun=newrun
    rval.insert(1,bestrun)
    return rval
def all_team_stats():
    qmkt="create table %s (Dvn varchar(10),Team varchar(35),F_R decimal(4,2),B_FR decimal(4,2),H_R decimal(4,2),B_HR decimal(4,2),A_R decimal(4,2),B_AR decimal(4,2))" % (FILENAME)
    nulv = run_query("Leagues",qmkt,"U")
    query='select Team,lg1 from teams where lg1 !="NA"'
    teams = run_query("Results",query,"Q")
    for row in teams:
	cons1=season_run("Teams",row[0])
	cons2=season_run_home("Teams",row[0])
	cons3=season_run_away("Teams",row[0])
        merged=cons1+cons2+cons3
	# Team, League, All consistency form + best run, Home, Away
	query="insert into %s (Dvn,Team,F_R,B_FR,H_R,B_HR,A_R,B_AR) values ('%s','%s','%s','%s','%s','%s','%s','%s')" % (FILENAME,row[1],row[0],round(merged[0],2),round(merged[1],2),round(merged[2],2),round(merged[3],2),round(merged[4],2),round(merged[5],2))
	#print(row[1],row[0], merged)
	run_query("Leagues",query,"U")
total = len(sys.argv)
if total > 1:
    FILENAME=str(sys.argv[1])
else:
    FILENAME="run_table"
all_team_stats()
