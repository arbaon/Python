#!/bin/bash
COUNT=0
FCOUNT=0
while read line 
do 
	A=$(echo $line | cut -d' ' -f1)
	B=$(echo $line | cut -d' ' -f2) 
	if [ $A -gt 0 ]; then
	    if [ $B != "NULL" ]; then
		echo $B
		if [ $B -gt 0 ]; then
			((COUNT ++))
		fi
		fi
	elif [ $A -lt 0 ]; then
	    if [ $B != "NULL" ]; then
		if [ $B -lt 0 ]; then
			((COUNT++))
		fi
		fi
	else
	    if [ $B != "NULL" ]; then
		if [ $B -eq 0 ]; then
			((COUNT++))
		fi
		fi
	fi
	if [ $B != "NULL" ]; then
	((FCOUNT++))
	fi
done <<< "$(mysql -uroot Predict -e "select tot,result from predict" | sed 1d)"
PERCENT=$(bc <<< "scale=2; $COUNT/$FCOUNT * 100")
echo $COUNT "correct from $FCOUNT predictions $PERCENT %"
