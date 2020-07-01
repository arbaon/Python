#!/bin/bash
if [ ! -d ../data/predict ]; then
	mkdir ../data/predict
fi
if [ -f /tmp/predictions.csv ]; then
	rm /tmp/predictions.csv
fi
if [ -f /tmp/odds.csv ]; then
	rm /tmp/odds.csv
fi
FILENAME="predictions_$(date +%Y-%m-%d).csv"
FILENAME_ODDS="odds_$(date +%Y-%m-%d).csv"
FILENAME2="predictions_$(date +%Y-%m-%d).sql"
FILENAME_ODDS2="odds_$(date +%Y-%m-%d).sql"
FILENAME3="v_predictions_$(date +%Y-%m-%d).sql"
mysql -uroot Predict -e "SELECT * from predict INTO OUTFILE '/tmp/predictions.csv' FIELDS TERMINATED BY ','"
mysql -uroot Predict -e "SELECT * from predict_odds INTO OUTFILE '/tmp/odds.csv' FIELDS TERMINATED BY ','"
mysqldump -uroot Predict predict > ../data/predict/$FILENAME2
mysqldump -uroot Predict predict_view > ../data/predict/$FILENAME3
mysqldump -uroot Predict predict_odds > ../data/predict/$FILENAME_ODDS2
mv /tmp/predictions.csv ../data/predict/$FILENAME
mv /tmp/odds.csv ../data/predict/$FILENAME_ODDS
sed -i 's/,\\N//g' ../data/predict/$FILENAME

