#!/bin/bash
USER="root"
PASS=""
DB="Results"
DBT="Teams"
DBL="Leagues"


#testing table generations
mysql -u$USER $DBL -e "select Divn,Team,HPlayed as HP,HWon as HW,HDrawn as HD,HLost as HL,HFor as HF, HAgainst as HA,HGD,APlayed as AP, AWon as AW,ADrawn as AD,ALost AL, AFor as AF,AAgainst as AG,(HGD+AGD) as \"GD\",Pts,@i:=@i+1 Pos from (Select @i:=0) as i,2016_league_table where Divn=\"E2\" order by Pts desc, GD desc"
mysql -u$USER $DBL -e "select Divn,Team,HPlayed as HP,HWon as HW,HDrawn as HD,HLost as HL,HFor as HF, HAgainst as HA,HGD,APlayed as AP, AWon as AW,ADrawn as AD,ALost AL, AFor as AF,AAgainst as AG,(HGD+AGD) as \"GD\",Pts,Pos from 2016_league_table where Divn=\"E2\" order by Pos"
mysql -u$USER $DBL -e "select *,HGD+AGD as GD,@i:=@i+1 Pos from (select @i:=0) as i,2016_league_table where Divn=\"E2\" order by Pts desc, GD desc"
#testing short table generation
mysql -u$USER $DBL -e "select Divn as Premier,Team,(HPlayed+APlayed) as P,(Hwon+Awon) as W,(HDrawn+ADrawn) as D,(HLost+ALost) as L,(HFor+AFor) as F,(HAgainst+AAgainst) as A,(HGD+AGD) as GD,Pts,@i:=@i+1 pos from (Select @i:=0) as i,2016_league_table where Divn=\"E0\" order by Pts desc, GD desc"
# Testing league table of home performance
mysql -u$USER $DBL -e "select Divn as D,Team as T,HPlayed as P, HWon as W, HDrawn as D, HLost as L, HFor as F,AAgainst as A, HGD as GD,HPts as Points,@i:=@i+1 Pos from (select @i:=0) as i,2016_league_table where Divn=\"E0\" order by HPts desc, GD desc"
#Full on table
mysql -u$USER $DBL -e "select Team,HPlayed as HP,HWon as HW,HDrawn as HD,HLost as HL,HFor as HF, HAgainst as HA,HGD,APlayed as AP, AWon as AW,ADrawn as AD,ALost AL, AFor as AF,AAgainst as AG,(HGD+AGD) as \"GD\",Pts,@i:=@i+1 Pos from (Select @i:=0) as i,2016_form_table where Divn=\"SP2\" order by Pts desc, GD desc"
# weight table
mysql -u$USER $DBL -e "select divn,team,pl,(acc+gbon+bon) as totes,hpl,(hacc+hgbon+hbon) as htotes,apl,(aacc+agbon+abon) as atotes from 2016_weight_table where divn=\"E0\" order by htotes desc"
mysql -u$USER $DBL -e "select * from recent_form where Divn =\"F1\" order by pts desc"
