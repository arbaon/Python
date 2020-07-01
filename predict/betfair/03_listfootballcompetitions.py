#!/bin/python
import requests
import json
import sys
 
endpoint = "https://api.betfair.com/exchange/betting/rest/v1.0/"
Token=str(sys.argv[1]) 
App = "yRamQ55REiQixmCP"
header = { 'X-Application' : App, 'X-Authentication' : Token ,'content-type' : 'application/json' }

json_req='{"filter":{"eventTypeIds": [1] }}'
 
url = endpoint + "listCompetitions/"
 
response = requests.post(url, data=json_req, headers=header)
 
 
print json.dumps(json.loads(response.text), indent=3)
