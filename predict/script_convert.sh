#!/bin/bash
#vars
OPTION=""
OSX="osx_setup.sh"
LNX="linux_setup.sh"
TMP="tmp_setup.sh"
#functions
function menu {
echo "Select either option 1) or 2)"
echo ""
echo "1) osx to linux"
echo "2) linux to osx"
echo ""
echo "note: the output script will be called tmp_setup.sh"
echo "      please test the script before renaming"
echo ""
printf "Enter your choice: "; read OPTION
}

menu
  if [ $OPTION -gt 0 ] && [ $OPTION -lt 3 ]; then
    if [ $OPTION -eq 1 ]; then
      rm $TMP
      cp $OSX $TMP
      sed -i "s/sed -i ''/sed -i/g" $TMP
      sed -i "s/INFILE/LOCAL INFILE/g" $TMP
      sed -i "s/osx_weight_table.py/weight_table.py/g" $TMP
      sed -i "s/osx_run_table.py/run_table.py/g" $TMP
    
    else
      rm $TMP
      cp $LNX $TMP
      sed -i '' "s/sed -i/sed -i ''/g" $TMP
      sed -i '' "s/LOCAL INFILE/INFILE/g" $TMP
      sed -i '' "s/weight_table.py/osx_weight_table.py/g" $TMP
      sed -i '' "s/run_table.py/osx_run_table.py/g" $TMP
    fi
  else
    echo ""
    echo "Bad Value entered. Try again."
    echo "-----------------------------"
  fi
