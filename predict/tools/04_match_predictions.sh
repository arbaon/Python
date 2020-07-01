#!/bin/bash
if [ -f ../data/predict/$1 ]; then
cat ../data/predict/$1 | while read line
	do 
		REF=$(echo $line | cut -d',' -f1)
		TABLE="$(echo $line | cut -d',' -f2)_2017"
		DATE=$(echo $line | cut -d',' -f3)
		TEAMA=$(echo $line | cut -d',' -f4)
		TEAMB=$(echo $line | cut -d',' -f5)
		#QUERY="select R from $TABLE where KO=\"$DATE\" and H_Team=\"$TEAMA\""
		QUERY="Select if(R=\"H\",1,if(R=\"A\",-1,0)) as R from $TABLE where KO=\"$DATE\" and H_Team=\"$TEAMA\""
		#echo $QUERY
		RESULT=$(mysql -uroot Results -e "$QUERY" | tail -1)
		echo $REF $DATE $TEAMA $TEAMB $RESULT
		QUERY2="update predict set result=\"$RESULT\" where id=$REF"
		mysql -uroot Predict -e "$QUERY2"
	done
else
	echo "invalid file"
fi
