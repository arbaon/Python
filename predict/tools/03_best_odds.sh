#!/bin/bash

echo "Best Home Form"
echo "-------------------------------------------------"

mysql Predict -e "select dvn,KO,h_team,a_team,fib,gls,tot,goalpw,totpw,H,D,A from predict_view where tot >= 3 and KO > '2019-02-01' order by totpw,H,goalpw,fib" | sed 's/\t/,/g'
echo
echo "Best Away Form"
echo "-------------------------------------------------"

mysql Predict -e "select dvn,KO,h_team,a_team,fib,gls,tot,goalpw,totpw,H,D,A from predict_view where tot <= -3 and KO > '2019-02-01' order by totpw,H,goalpw,fib" | sed 's/\t/,/g'
echo
echo "Best Home Odds no less than 1/3 of price and opposition is at least 1/2 down"
echo "-------------------------------------------------"

mysql Predict -e "select dvn,KO,h_team,a_team,fib,gls,tot,goalpw,totpw,H,D,A from predict_view where H > 1.35 and tot >=0 and A > (H+0.5) and KO > '2019-02-01' order by totpw,H,goalpw,fib" | sed 's/\t/,/g'
echo
echo "Best Away Odds no less than 1/3 of price and opposition is at least 1/2 down"
echo "-------------------------------------------------"

mysql Predict -e "select dvn,KO,h_team,a_team,fib,gls,tot,goalpw,totpw,H,D,A from predict_view where A > 1.35 and tot <= -3 and H > (A+0.5) and KO > '2019-02-01' order by totpw,H,goalpw,fib" | sed 's/\t/,/g'
