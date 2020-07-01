#!/bin/bash
if [ -d "/home/bcorbett" ]; then
    homedir="/home/bcorbett/"
    user="bcorbett"
else
    homedir="/home/ec2-user"
    user="ec2-user"
fi
filename="my_bet_slip.csv"
function drop() 
{
mysql -uroot Predict -e "drop view if exists tmp_v1"
mysql -uroot Predict -e "drop view if exists tmp_v2"
mysql -uroot Predict -e "drop view if exists tmp_v3"
}
function views()
{
mysql -uroot Predict -e "create view tmp_v1 as select * from predict_view where tot > 0 order by tot desc,H"
mysql -uroot Predict -e "create view tmp_v2 as select * from predict_view where tot < 0 order by tot,H"
mysql -uroot Predict -e "create view tmp_v3 as select * from predict_view where tot = 0 order by H"
}

function create()
{
mysql -uroot Predict -e "select * from tmp_v1" > $filename
mysql -uroot Predict -e "select * from tmp_v2" | sed 1d >> $filename
mysql -uroot Predict -e "select * from tmp_v3" | sed 1d >> $filename
sed -i 's/\t/,/g' $filename
}

function movit ()
{
mv $filename $homedir
chown $user.$user $homedir/$filename
}

drop
views
create
drop
movit
