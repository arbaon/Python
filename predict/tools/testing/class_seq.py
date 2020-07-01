#!/usr/bin/python
import MySQLdb
class Sequence:
    def __init__(self):
        self.Sseq = [0.8,0.8,0.2]
        self.Sval = [0,0]
    def runseq(self,result):
        fseq = self.formseq()
	frun = self.formrun(result)
        sweight = fseq * result
	rweight = frun + sweight
	aweights = [frun,sweight,rweight]
	return aweights
    def formseq(self):
    	if self.Sseq[1] < self.Sseq[0]:
	    self.Sseq[1] = self.Sseq[0]
    	else:
	    self.Sseq[0] = self.Sseq[0] + self.Sseq[2]
	    print (self.Sseq[0],self.Sseq[1],self.Sseq[2])
	return self.Sseq[0]
    def formrun(self,result):
	if result == 3:
	    result = 2
    	if result > 0:
	    if self.Sval[0] > 1 and result == 1:
	        self.Sval[1] = self.Sval[1] - result
            else:
	    	self.Sval[1] = self.Sval[1] + result
	    self.Sval[0] = result
    	else:
	    self.Sval[1] = 0
	    self.Sval[0] = 0
	return self.Sval[1]

def get_seq(mresults):
    X = Sequence()
    totals = [0,0,0]
    nlbonus = 6
    opbonus = 0
    for num in range(0,18,3):
        mytest = X.runseq(mresults[num])
        totals = map(sum, zip(totals,mytest))
	pos=mresults[num+1]/7
	tpos=mresults[num+1]%7
	if pos < 1 and tpos > 0:
	    pos = 1
	elif pos == 1 and tpos > 0:
	    pos = 2
	elif pos == 2 and tpos > 0:
	    pos = 3 
        dif=mresults[num+2]
	tmpbonus=get_bonus(dif,pos)
	if mresults[num] == 0:
	    nlbonus = nlbonus - 1
        opbonus = opbonus + tmpbonus
    #return percentages.
    f1=format((totals[0]/42.0)*100,'.1f')
    f2=format((totals[2]/63.6)*100,'.1f')
    f4=format((opbonus/90.0)*100,'.1f')
    #totes=[totals[0],format(totals[2],'.1f'),nlbonus,opbonus]
    totes=[f1,f2,nlbonus,f4]
    print totes
    return totes
def get_bonus(dif,pos):
    reward = 0
    if dif < 0:
	if pos == 2 and dif > -2:
	    reward = 1
	if pos == 1 and dif > -2:
	    reward = 2
    if dif == 0:
	if pos == 3:
	    reward = 3
	if pos == 2:
	    reward = 5
	if pos == 1:
	    reward = 7
    if dif > 0:
    	if pos == 3:
            reward = 7 + (dif -1) * 1
        if pos == 2:
            reward = 9 + (dif -1) * 1
        if pos == 1:
            reward = 11 + (dif -1) * 2
    return reward
def upd_table(league,query):
    db=MySQLdb.connect(user="root", db=league)
    cur=db.cursor()
    cur.execute(query)
    db.commit()
    cur.close
    db.close

def run_query(league,query):
    db=MySQLdb.connect(user="root", db=league)
    cur=db.cursor()
    cur.execute(query)
    data=cur.fetchall()
    cur.close
    db.close
    return data
def short_tables(league,tbtype):
    limited = 6
    query="""select team from league_teams"""
    teamlist=run_query(league,query)
    query2="""drop table if exists short_%s""" % (tbtype)
    upd_table(league,query2)
    query3="""create table if not exists short_tmp (team varchar (20), won int, draw int, lost int,gfor int, gagainst int, diff int, points int)"""
    upd_table(league,query3)
    if tbtype == "league":
	limited = 50
    for row in teamlist:
	query4="""insert into short_tmp select "%s" as team,sum(if (Result="W",1,0)) as won, sum(if (Result="D",1,0)) as draw, sum(if (Result="L",1,0)) as lost, sum(GF) as gfor,sum(GA) as gagainst,sum(GF)-sum(GA) as diff,sum(if(Result="D",1,if(Result="W",3,0))) as points from (select * from `%s` order by kickoff desc limit %s) as temp;""" % (row[0],row[0],limited)
	upd_table(league,query4)
    query5="""create table short_%s select * from short_tmp order by points desc""" % (tbtype)
    upd_table(league,query5)
    query6="""alter table short_%s add pos int not null auto_increment primary key""" % (tbtype)
    upd_table(league,query6)
    query7="""drop table if exists short_tmp"""
    upd_table(league,query7)
def get_teams(league):
    query="""select team from league_teams"""
    teamlist=run_query(league,query)
    query2="""drop table if exists recent_form"""
    run_query(league,query2)
    query3="""create table if not exists recent_form (tm varchar(20),pts decimal(5,2),acc decimal(5,2),bon int, per decimal(5,2),hpts decimal(5,2),hacc decimal(5,2),hbon int,hper decimal(5,2),apts decimal(5,2),aacc decimal(5,2),abon int,aper decimal(5,2),runs int,hruns int, aruns int)"""
    upd_table(league,query3) 
    for row in teamlist:
	tmp=[row[0]]
        tmp=tmp + last_six(league,row[0])
	tmp=tmp + last_six_home(league,row[0])
	tmp=tmp + last_six_away(league,row[0])
	#season_run(league,row[0])
	tmp=tmp + season_run(league,row[0])
	tmp=tmp + season_run_home(league,row[0])
	tmp=tmp + season_run_away(league,row[0])
	query4="insert into recent_form (tm,pts,acc,bon,per,hpts,hacc,hbon,hper,apts,aacc,abon,aper,runs,hruns,aruns) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (tmp[0],tmp[1],tmp[2],tmp[3],tmp[4],tmp[5],tmp[6],tmp[7],tmp[8],tmp[9],tmp[10],tmp[11],tmp[12],tmp[13],tmp[14],tmp[15])	
	upd_table(league,query4)
    #tmptb="form"
    short_tables(league,"form")
    short_tables(league,"league")
def last_six(league,team):
    query="""select kickoff as ko,if(result='W',3,if(result='D',1,0)) as res,pos,gf-ga as dif from `%s` order by kickoff desc limit 6""" % (team)
    results=run_query(league,query)
    seqnc = []
    rseqnc = []
    for row in results:
	seqnc.append(int(row[1]))
	seqnc.append(int(row[2]))
	seqnc.append(int(row[3]))
    rseqnc=get_seq(seqnc)
    return rseqnc	
def last_six_home(league,team):
    query="""select kickoff as ko,if(result='W',3,if(result='D',1,0)) as res,pos,gf-ga as dif from `%s` where fixture='H' order by kickoff desc limit 6""" % (team)
    results=run_query(league,query)
    seqnc = []
    for row in results:
	seqnc.append(int(row[1]))
	seqnc.append(int(row[2]))
	seqnc.append(int(row[3]))
    rseqnc=get_seq(seqnc)
    return rseqnc	

def last_six_away(league,team):
    query="""select kickoff as ko,if(result='W',3,if(result='D',1,0)) as res,pos,gf-ga as dif from `%s` where fixture='A' order by kickoff desc limit 6""" % (team)
    results=run_query(league,query)
    seqnc = []
    for row in results:
	seqnc.append(int(row[1]))
	seqnc.append(int(row[2]))
	seqnc.append(int(row[3]))
    rseqnc=get_seq(seqnc)
    return rseqnc	
def season_run(league,team):
    query="""select if(Result='L',0,1) as seq from `%s`""" % (team)
    results=run_query(league,query)
    rval=[]
    scount=0
    lrow=0
    for row in results:
	if row[0] == 0:
	    scount=scount+1
        else:
	    if lrow == 0:
		scount=scount+1
	lrow = row[0]
    rval.insert(0,scount)
    return rval
	   
def season_run_home(league,team):
    query="""select if(Result='L',0,1) as seq from `%s` where Fixture='H'""" % (team)
    results=run_query(league,query)
    rval=[]
    scount=0
    lrow=0
    for row in results:
	if row[0] == 0:
	    scount=scount+1
        else:
	    if lrow == 0:
		scount=scount+1
	lrow = row[0]
    rval.insert(0,scount)
    return rval

def season_run_away(league,team):
    query="""select if(Result='L',0,1) as seq from `%s` where Fixture='A'""" % (team)
    results=run_query(league,query)
    rval=[]
    scount=0
    lrow=0
    for row in results:
	if row[0] == 0:
	    scount=scount+1
        else:
	    if lrow == 0:
		scount=scount+1
	lrow = row[0]
    rval.insert(0,scount)
    return rval

#get_teams("premier")
#get_teams("championship")
#get_teams("divone")
#get_teams("divtwo")
#get_teams("conference")
#get_teams("bundesliga1")
#get_teams("bundesliga2")
#get_teams("scotprem")
#get_teams("scotchamp")
#get_teams("scotone")
#get_teams("scottwo")
#get_teams("seriea")
#get_teams("serieb")
#get_teams("ligue1")
#get_teams("ligue2")
#get_teams("liga1")
#get_teams("liga2")
#get_teams("primeira")
#get_teams("eredivisie")
#get_teams("bdivone")
seqnct=[1,1,1,3,1,1,3,1,1,3,1,1,0,1,-1,3,1,1]
get_seq(seqnct)
