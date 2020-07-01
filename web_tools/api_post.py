#! /usr/bin/python
import json
import requests
r = requests.post('http://httpbin.org/post', files=dict(foo='bar'))
print (r.status_code)
print (r.json()['headers'])
print (r.url)
