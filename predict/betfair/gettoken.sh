#!/bin/bash

KEYNAME="arbaon-2048.key"
USERNAME="arbaon"
PASSWORD="m1llwall"

curl -k -i -H "Accept: application/json" -H "X-Application: $KEYNAME" -X POST -d "username=$USERNAME&password=$PASSWORD" https://identitysso.betfair.com/api/login
