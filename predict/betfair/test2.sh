#!/bin/bash
#curl -v https://api.betfair.com/exchange/betting/rest/v1.0/listEventTypes/ -H "X-Application : yRamQ55REiQixmCP" -H "X-Authentication : $1" -H "content-type : application/json" --data '{"filter":{ }}' | jq .
curl -v https://api.betfair.com/exchange/betting/rest/v1.0/listMarketBook/ -H "X-Application : yRamQ55REiQixmCP" -H "X-Authentication : $1" -H "content-type : application/json" --data '{"marketIds": ["1.194215"], "priceProjection": { "priceData": ["EX_BEST_OFFERS", "EX_TRADED"], "virtualise": "true"} }' | jq .
