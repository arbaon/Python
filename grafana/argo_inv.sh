#!/bin/bash
#
# argo_inv.sh 
# 
# This script scrapes "argo" components and creates a basic dashboard/s from a json template to upload to grafana
#
# Author: Bill Corbett
#

# Variables
# ---------
 
BASEDIR=$( cd $(dirname $0) ; pwd -P )
JSON_START="\"targets\": [ "
JSON_END="],"
JSON_TEMPLATE="argo_inv_tpl.json"
JSON_FILES="/tmp/grafana_import"
DEFAULT_ENV="staging milan prod"
DEFAULT_TAG="\"tags\": [],"
CNP=0; GRA=0; ALL=0
TAGS=$DEFAULT_TAG

# Functions
# ---------

# Loops through Argo and pulls the instances from components. Populates a grafana template with the host details for each component.
#

function environments {
  for ENV in $DEFAULT_ENV
    do 
      if [ "$2" == "" ]; then
        COMPLIST=$(curl -sk https://argo.chronos.hcom/environment/$ENV/components/ | jq '.components[].value.shortName' | sed 's/"//g') 
      elif [ $1 -lt 1 ]; then
	COMPLIST=$(curl -sk https://argo.chronos.hcom/environment/$ENV/components/ | jq '.components[].value.shortName' | sed 's/"//g' | grep "$2")
      else
	COMPLIST=$2
      fi
        for COMP in $COMPLIST
          do
	    echo $ENV"_"$COMP
	    echo "-----------"
              for INST in $COMP
	        do
		  ITOTAL=$(curl -sk https://argo.chronos.hcom/environment/$ENV/component/$COMP/instances | jq '.instances[].value.server' | wc -l)
		  MEM_BUFF="";CPU_BUFF="";DISK_BUFF="";DESC_BUFF="";ICOUNT=0
		  if [ $ITOTAL -gt 0 ]; then
		    curl -sk https://argo.chronos.hcom/environment/$ENV/component/$COMP/instances | jq '.instances[].value.server' | sed 's/"//g' | while read line		    
	            do
		      IHOST=$(echo $line | cut -d'.' -f1)
		      ICOUNT=$(($ICOUNT+1))
	                if [ $ICOUNT -eq $ITOTAL ]; then COMMA=0; else COMMA=1; fi
		      ID="";alpha $ICOUNT
		      buffers $ID  $IHOST $COMMA
		        if [ $ICOUNT -eq $ITOTAL ]; then 
		          MEMJSON="$JSON_START$MEM_BUFF$JSON_END"
		          CPUJSON="$JSON_START$CPU_BUFF$JSON_END"
		          DISKJSON="$JSON_START$DISK_BUFF$JSON_END"
		          DESCJSON="$JSON_START$DESC_BUFF$JSON_END"
			  TITLE="\"title\": \"$ENV $COMP : Stats\","
			  FLNM=$JSON_FILES/$ENV"_"$COMP.json
			  QTAG=$(echo $COMP | cut -d"_" -f1)
			  add_tag $ENV $QTAG
			  cat $BASEDIR/$JSON_TEMPLATE | sed "s@NEW_TITLE@$TITLE@g" | sed "s@NEW_TAGS@$TAGS@g" | sed "s@TARGET_MEMORY@$MEMJSON@g" | sed "s@TARGET_CPU@$CPUJSON@g" | sed "s@TARGET_DISK@$DISKJSON@g" | sed "s@TARGET_DESCRIPTORS@$DESCJSON@g" > $JSON_FILES/$ENV"_"$COMP.json
			  if [ $3 -gt 0 ]; then
			    import_graph $FLNM $ENV
		          fi
		        fi	
	            done
		  else
		    echo "No instances"
		  fi
	        done
           done		  
    done
}
# formats and concatenates the json string
# ref 1=refid, 2=host, 3=comma
function buffers {
  TMP_MEM="\"refId\": \"$1\", \"target\": \"sensu.$2.memory.*\"}"
  TMP_CPU="\"refId\": \"$1\", \"target\": \"sensu.$2.cpu.*\"}"
  TMP_DSK="\"refId\": \"$1\", \"target\": \"aliasByNode(sensu.$2.root.hcom.used_percentage,1)\"}"
  TMP_DCP="\"refId\": \"$1\", \"target\": \"aliasByNode(sensu.$2.descriptors.*,1)\"}"
    if [ $3 -eq 1 ]; then 
      FMT=","
      FFMT="{ "
    else 
      FMT=""
      FFMT="{ \"hide\": false,"
    fi
  MEM_BUFF=$MEM_BUFF$FFMT$TMP_MEM$FMT
  CPU_BUFF=$CPU_BUFF$FFMT$TMP_CPU$FMT
  DISK_BUFF=$DISK_BUFF$FFMT$TMP_DSK$FMT
  DESC_BUFF=$DESC_BUFF$FFMT$TMP_DCP$FMT
}
# returns a character by number 1=a 2=b etc..
function alpha {
  ALP="ABCDEFGHIJKLMNNOPQRSTUVWYX"
  MOD=$(($1-1))
  ID=${ALP:$MOD:1}
}
# imports the json file into grafana runs python script
function import_graph {
  echo "Upload to grafana"
    if [ "$2" == "prod" ]; then 
      HEAD="Authorization: Bearer eyJrIjoiTXVUc1BSS0UzWXBMdUQ4YklhNWttTmN0M0pNM0p5bmwiLCJuIjoidGVjaG9wcyIsImlkIjoxfQ=="
      URL="https://dashboard.prod.hcom/api/dashboards/db"
    else
      HEAD="Authorization: Bearer eyJrIjoiakc2MEdQelhPQjBpRTQwSUo4bXZTandSa25ySkxmV2YiLCJuIjoidGVjaG9wcyIsImlkIjoxfQ=="
      URL="https://dashboard.lab.hcom/api/dashboards/db"
    fi
  curl -k -X POST $URL -d @$1 -H "Accept: application/json" -H "Content-Type: application/json" -H "$HEAD"  
  
}
function add_tag {
  if [[ $1 == "milan" || $1 == "staging" || $1 == "prod" ]]; then
    if [[ $2 == "zk" || $2 == "kafka" || $2 == "redis" || $2 == "cassandra" ]]; then
      CTAG="datainf_"$2
      TAGS="\"tags\": [\"$1\",\"$CTAG\"],"	
    else
      TAGS=$DEFAULT_TAG
    fi
  else
    TAGS=$DEFAULT_TAG 
  fi
}
function disclaimer {
  echo
  echo -e "\t\t\tHow to use this script"
  echo -e "\t\t---------------------------------------------------"
  echo
  echo -e "\t\tGeneral"
  echo -e "\t\targo_inv.sh -a -c -g <component/regex> <environment>"
  echo -e "\t\teg. argo_inv.sh -c -g kafka_new staging"
  echo
  echo -e "\t\tFlags"
  echo -e "\t\t-a will run all environments when there are no args"
  echo -e "\t\t-c will run the individual component arg(1) in environment arg(2)"
  echo -e "\t\t-g will import the json file/s into grafana, generated files are kept in /tmp"
  echo
  echo -e "\t\tArgs"
  echo -e "\t\t(1) if \"-c\" is not included arg(1) will match components by name"
  echo -e "\t\t(2) desired environment. not included after arg(1) will default to staging"
  echo
  echo -e "\t\t----------------------------------------------------"
  echo
}
# Check flags
  if [ ! -d $JSON_FILES ]; then
    mkdir $JSON_FILES
  fi
  while getopts :acg flag
    do
      case $flag in
        c)CNP=1;;
        g)GRA=1;;
        a)ALL=1;;
       *);;
      esac
   done
shift $(($OPTIND -1))
# check arguments
  if [ "$2" != "" ]; then
    DEFAULT_ENV=$2
  elif [ $CNP -gt 0 ]; then
    DEFAULT_ENV="staging"
  fi
    if [ $# -lt 1 ] && [ $ALL -lt 1 ]; then
      disclaimer
    else
      environments $CNP $1 $GRA
    fi
