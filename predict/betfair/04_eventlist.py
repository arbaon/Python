#!/bin/python
import requests
import json
import sys
 
endpoint = "https://api.betfair.com/exchange/betting/rest/v1.0/"
Token=str(sys.argv[1]) 
App = "yRamQ55REiQixmCP"
header = { 'X-Application' : App, 'X-Authentication' : Token ,'content-type' : 'application/json' }
url = endpoint + "listEvents/" 

mycompetition = {
    "E0" : 10932509,
    "E1" : 7129730,
    "E2" : 35,
    "E3" : 37,
    "EC" : 11086347,
    "SC0" : 105,
    "SC1" : 107,
    "SC2" : 109,
    "SC3" : 111,
    "D1" : 59,
    "I1" : 81,
    "I2" : 83,
    "P1" : 99,
    "N1" : 9404054,
    "F1" : 55,
    "SP1": 117
}
for k,v in mycompetition.iteritems():
    print k
    json_req='{"filter":{"competitionIds": [%s], "marketStartTime": {"from": "2018-12-27T00:00:00Z","to": "2019-01-31T23:59:00Z"}},"maxResults":1000}' % v
    response = requests.post(url, data=json_req, headers=header)
    test=json.loads(response.text)
    for lp in test:
        print ("%s,%s,%s,%s,%s,%s") % (k,lp['event']['timezone'],lp['event']['openDate'],lp['event']['id'],lp['event']['countryCode'],lp['event']['name'])

#    print json.dumps(json.loads(response.text), indent=3)
