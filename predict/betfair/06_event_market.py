#!/bin/python
import requests
import json
import sys
 
endpoint = "https://api.betfair.com/exchange/betting/rest/v1.0/"
Token=str(sys.argv[1]) 
App = "yRamQ55REiQixmCP"
header = { 'X-Application' : App, 'X-Authentication' : Token ,'content-type' : 'application/json' }

json_req='{"marketIds": ["1.152769696"], "priceProjection": { "priceData": ["EX_BEST_OFFERS", "EX_TRADED"], "virtualise": "true"} }'
#json_req='{"marketIds": ["1.152769696"] }'

#(1)
#json_req='{"filter":{"eventIds": [29055070],"marketTypeCodes": ["MATCH_ODDS"]},"maxResults":1000,"marketProjection": ["RUNNER_DESCRIPTION"]}'
#url = endpoint + "listMarketCatalogue/"
url = endpoint + "listMarketBook/"
#url = endpoint + "listEvents/"
 
response = requests.post(url, data=json_req, headers=header)
test=json.loads(response.text)
#for lp in test:
#    print ("%s,%s,%s,%s,%s") % (lp['event']['timezone'],lp['event']['openDate'],lp['event']['id'],lp['event']['countryCode'],lp['event']['name'])

print json.dumps(json.loads(response.text), indent=3)
