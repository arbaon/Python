#!/usr/bin/python
import MySQLdb
import sys
#
# 1) League Pos
# 2) League Tier
# 3) Form Pos
# 4) Form Tier
# 5) League Perf
# 6) Form Perf
# 7) Weight all
# 8) Weight H/A
# 9) Fib number
# 10) Fib count
# 11) Goals F
# 12) Goals A
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
def get_members(dv):
   query="""select Members from competitions where CID="%s" """ % (dv)
   result=run_query("Results",query,"Q")
   return result[0][0]
def get_pos(year,tab,team):
    query="""select Pos from %s_%s_table where team="%s" """% (year,tab,team)
    results=run_query("Leagues",query,"Q")
    tmp=int(results[0][0])
    return tmp
def get_state(Top,Mid,Place):
    if Place <= Top:
	return 1
    elif Place <= Mid:
	return 2
    else:
	return 3
def get_goals(year,team,ha):
    
    if ha=="away":
	G="A_G"
        GA="A_GA"
    else:
 	G="H_G"
	GA="H_GA"
    query="""select %s,%s from %s_ha_play_table where team="%s" """ %(G,GA,year,team)
    results=run_query("Leagues",query,"Q")
    gls=[float(results[0][0]),float(results[0][1])]
    return gls
def get_perform(year,tier,ha,team):
    
    if tier==1:
	if ha=="away":
	    col="apt"
        else:
	    col="hpt"
    elif tier==2:
	if ha=="away":
	    col="apm"
        else:
	    col="hpm"
    else:
	if ha=="away":
	    col="apb"
	else:
	    col="hpb"
    query="""select %s from %s_mega_perform where team="%s" """ %(col,year,team)
    results=run_query("Leagues",query,"Q")
    tmp=float(results[0][0])
    return tmp	    
def get_weight(year,ha,team):
    weight=[]
    query="""select ((acc / 6) + gbon + bon) / 3 as AL, ((hacc / 6) + hgbon + hbon) / 3 as H,((aacc / 6) + agbon + abon) / 3 as A from %s_weight_table where team="%s" """ %(year,team)	
    results=run_query("Leagues",query,"Q")
    tmp=float(results[0][0])
    if ha=="home":
    	tmp1=float(results[0][1])
    else:
    	tmp1=float(results[0][2])
    weight.append(tmp)
    weight.append(tmp1)
    return weight   
def get_fib(team,fix):
    if fix =="all":
        query="""select if(R="L",0,1) as RT from (select if( R="D","D",if(H_team="%s",if(R="H","W","L"),if(R="A","W","L"))) as R from `%s` order by KO desc limit 40) as RES"""% (team,team)
    else:
        query="""select if(R="L",0,1) as RT from (select if( R="D","D",if(H_team="%s",if(R="H","W","L"),if(R="A","W","L"))) as R from `%s` where %s="%s" order by KO desc limit 40) as RES"""% (team,team,fix,team)
    results=run_query("Teams",query,"Q")
    rval=0
    pval=[]
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
        rval=newval
    pval.append(rval)
    tval=rval
    tcnt=0
    while (tval > 1.5):
        tval=tval/PHI
        tcnt=tcnt+1
    pval.append(tcnt)
    return pval
def fib_fun(val):
    tval=val
    tcnt=0
    fib=1.618
    while (tval > 1.5):
	tval=tval/fib
        tcnt=tcnt+1
    return tcnt
def uni_conv(val,typ):
    global rw
    if val > rw[typ][0]:
        ADV=3
    elif val > rw[typ][1]:
        ADV=2
    elif val > rw[typ][2]:
        ADV=1
    elif val < -rw[typ][0]:
        ADV=-3
    elif val < -rw[typ][1]:
        ADV=-2
    elif val < -rw[typ][2]:
        ADV=-1
    else:
        ADV=0
    return ADV
def init():
    TeamA=[];TeamB=[];YR="2017"
    ID=str(sys.argv[1])
    Divn=str(sys.argv[3])
    Date=str(sys.argv[2])
    Top=get_members(Divn)/3
    Mid=Top+Top+1
    TeamA.append(str(sys.argv[4]))#Team Name
    TeamB.append(str(sys.argv[5]))#Team Name
    for LF in ["league","form"]:
    	TeamA.append(get_pos(YR,LF,TeamA[0]))#Pos
    	TeamB.append(get_pos(YR,LF,TeamB[0]))#Pos
    	TeamA.append(get_state(Top,Mid,TeamA[-1]))#Tier
    	TeamB.append(get_state(Top,Mid,TeamB[-1]))#Tier
    for MG in [2,4]:
    	TeamA.append(get_perform(YR,TeamB[MG],"home",TeamA[0]))#perform
    	TeamB.append(get_perform(YR,TeamA[MG],"away",TeamB[0]))#perform
    TeamA = TeamA + get_weight(YR,"home",TeamA[0])#weight
    TeamB = TeamB + get_weight(YR,"home",TeamB[0])#weight
    TeamA = TeamA + get_fib(TeamA[0],"H_Team")#fib
    TeamB = TeamB + get_fib(TeamB[0],"A_Team")#fib
 
    TeamA = TeamA + get_goals(YR,TeamA[0],"home")#goals
    TeamB = TeamB + get_goals(YR,TeamB[0],"away")#goals

    predict(TeamA,TeamB,Top,Divn,Date,ID)
def predict(TeamA,TeamB,Top,dvn,ko,ID):
    lp=float(TeamA[1]-TeamB[1])/Top
    fp=float(TeamA[3]-TeamB[3])/Top
    lp=lp*-1
    fp=fp*-1
    pfl=TeamA[5]-TeamB[5]
    pff=TeamA[6]-TeamB[6]
    WA=TeamA[7]-TeamB[7]
    WHA=TeamA[8]-TeamB[8]
    fiba=float(fib_fun(TeamA[9]))/10
    fibb=float(fib_fun(TeamB[9]))/10
    FIB=fiba-fibb
    GLS=(TeamA[11]+TeamB[12])-(TeamB[11]+TeamA[12]) 
    tmpa=uni_conv(lp,0)  # league pos
    tmpb=uni_conv(fp,0)  # form pos
    tmpc=uni_conv(pfl,1) # league perform
    tmpd=uni_conv(pff,1) # form perform
    tmpe=uni_conv(WA,2)  # weight all
    tmpf=uni_conv(WHA,2) # weight h/a
    tmpg=uni_conv(FIB,3) # touch of green
    tmph=uni_conv(FIB,4) # goals
    tot=(tmpa+tmpc+tmpe)+((tmpb+tmpd+tmpf+tmpg+tmph)*1.2)
    tmpi=uni_conv(tot,5)
    print tmpa,tmpb,tmpc,tmpd,tmpe,tmpf,tmpg,tmph,tmpi
    if str(sys.argv[6]) == "y":
    	#query="insert into %s (dvn,KO,h_team,a_team,lp,fp,lpf,fpf,wa,wha,fib,gls,tot) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % ("Predict",dvn,ko,TeamA[0],TeamB[0],tmpa,tmpb,tmpc,tmpd,tmpe,tmpf,tmpg,tmph,tmpi)
    	query="update %s set lp=%s,fp=%s,lp=%s,fpf=%s,wa=%s,wha=%s,fib=%s,gls=%s,tot=%s where ID=%s" % ("Predict",tmpa,tmpb,tmpc,tmpd,tmpe,tmpf,tmpg,tmph,tmpi,ID)
    	run_query("Predict",query,"U")
    #print TeamA
    #print TeamB
    #print tmpa,tmpb
    #print tmpc,tmpd
    #print tmpe,tmpf
    #print tmpg,tmph
total = len(sys.argv)
if total > 1:
    rw=[]
    rw.append([1.5,1,0.5])
    rw.append([1.7,1.2,0.7])
    rw.append([5,3,1.5])
    rw.append([3,2,1])
    rw.append([1.9,1.2,0.5])
    rw.append([20,13,5])
    init()
else:
    print("No Information provided!")
