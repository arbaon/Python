#!/usr/local/bin/python
import MySQLdb
import sys
def run_query(DTB,query,type):
    if type !="U":
        type = "Q"
    db=MySQLdb.connect(user="root", db=DTB)
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
def run_fib(league,team):
    query="""select if(R="L",0,1) as RT from (select if( R="D","D",if(H_team="%s",if(R="H","W","L"),if(R="A","W","L"))) as R from `%s` order by KO desc limit 40) as RES"""% (team,team)
    results=run_query(league,query,"Q")
    rval=[]
    tmpval=[]
    acount=0
    lcount=0
    PHI=1.618
    for row in results:
        acount=acount+1
        if row[0] == 0:
	    if lcount == 0:
		newval=0
	    else:
		newval=round(lcount/PHI)
		lcount=newval
        else:
	    if lcount == 0:
                newval=1
		lcount=newval
	    else:
		newval=round(lcount*PHI)
		lcount=newval
	tmpval="[\"{}\",{}]".format(newval,acount)
    	rval.append(tmpval)
    #print (lcount/acount)
    return rval
       
def test():
    step_one=[]
    step_one=run_fib("Teams","Arsenal")
    step_two= "[%s]" % (','.join(step_one))
    fib=step_two.replace('\"','\'')
    print fib
test()
