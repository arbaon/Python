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
def run_fib(team,fix):
    if fix=="all":
    	query="""select if(H_Team="%s",if(R="H",3,if(R="D",1,0)),if(R="A",3,if(R="D",1,0))) as RT from `%s` order by KO asc limit 40""" % (team,team)
    else:
    	query="""select if(H_Team="%s",if(R="H",3,if(R="D",1,0)),if(R="A",3,if(R="D",1,0))) as RT from `%s` where %s="%s" order by KO asc limit 40""" % (team,team,fix,team)
    results=run_query("Teams",query,"Q")
    rval=[]
    tmpval=[]
    acount=0
    lcount=0
    for row in results:
        acount=acount+1
        if int(row[0]) < 1:
	    newval=lcount-3
	    lcount=newval
        else:
	    newval=lcount+row[0]
            lcount=newval
	tmpval="[\"{}\",{}]".format(acount,newval)
    	rval.append(tmpval)
    return rval
       
def graphit(team):
    step_one=[]
    step_one=run_fib(team,"all")
    step_two= "[%s]" % (','.join(step_one))
    fib=step_two.replace('\"','')
    print fib
total = len(sys.argv)
if total > 1:
    team=str(sys.argv[1])
    graphit(team)
