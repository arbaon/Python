#!/usr/local/bin/python
import MySQLdb
import sys
def run_query(league,query):
    db=MySQLdb.connect(user="root", db=league)
    cur=db.cursor()
    cur.execute(query)
    data=cur.fetchall()
    cur.close
    db.close
    return data
def season_run(league,team):
    query="""select if(R="L",0,1) as RT from (select if( R="D","D",if(H_team="%s",if(R="H","W","L"),if(R="A","W","L"))) as R from `%s` order by KO desc limit 40) as RES"""% (team,team)
    results=run_query(league,query)
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
    #rval.insert(0,scount)
    #rval.insert(1,acount)
    #rval.insert(2,perct)
    rval.insert(0,perct)
    if newrun > bestrun:
	bestrun=newrun
    rval.insert(1,bestrun)
    return rval
       
def season_run_home(league,team):
    query="""select if(R="L",0,1) as RS from (select if(R="H","W",if(R="D","D","L")) as R from `%s` where H_Team = "%s" order by KO desc limit 20 ) as RES""" % (team,team)
    results=run_query(league,query)
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
    #rval.insert(0,scount)
    #rval.insert(1,acount)
    #rval.insert(2,perct)
    rval.insert(0,perct)
    if newrun > bestrun:
	bestrun=newrun
    rval.insert(1,bestrun)
    return rval

def season_run_away(league,team):
    query="""select if(R="L",0,1) as RS from (select if(R="A","W",if(R="D","D","L")) as R from `%s` where A_Team = "%s" order by KO desc limit 20 ) as RES""" % (team,team)
    results=run_query(league,query)
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
    #rval.insert(0,scount)
    #rval.insert(1,acount)
    #rval.insert(2,perct)
    rval.insert(0,perct)
    if newrun > bestrun:
	bestrun=newrun
    rval.insert(1,bestrun)
    return rval
def all_team_stats():
    query='select Team,lg1 from teams where lg1 !="NA"'
    teams = run_query("Results",query)
    for row in teams:
	plod1=season_run("Teams",row[0])
	plod2=season_run_home("Teams",row[0])
	plod3=season_run_away("Teams",row[0])
        merged=plod1+plod2+plod3
	print(row[0],row[1], merged)
all_team_stats()
