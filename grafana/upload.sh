#!/bin/bash
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
  curl -v -k -X POST $URL -d @$1 -H "Accept: application/json" -H "Content-Type: application/json" -H "$HEAD"
}
import_graph ./test.json lab
