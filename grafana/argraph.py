#!/usr/local/bin/python
import json,re,subprocess,time
import os
import sys
import httplib2
from sys import argv

#globals
rowidx=0
panidx=1
environment=""
component=""

#functions

#get arguments for argo environment and component
def fileopt():
    global environment,component
    if len(argv) > 3:
        gtype = argv[3]
    else:
        gtype = "all"
    if len(argv) > 2:
        environment = argv[1]
        component = argv[2]
    else:
        print "Invalid Arguments: argraph.py <environment> <component> <optional dashtype>"
        sys.exit()
    return gtype
#Add a row to the dashboard
def rowadd(base):
    global rowidx
    null=None
    base['dashboard']['rows'].append({ "collapse": False,"height": 250, "panels": [],"repeat": null, "repeatIteration": null, "repeatRowId": null, "showTitle": False, "title": "Dashboard Row","titleSize": "h6" },)
    rowidx += 1
    return base

#Add a panel to a row
def paneladd(base,row,hosts,service,item,app,spanl):
    global panidx, environment
    refid=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T"]
    pname = app+" :: "+service
    if len(hosts) > 1:
        pname = app+" :: "+service
    else:
        if environment != "null":
            pname = app+" : "+hosts[0]+" : "+service
        else:
            pname= hosts[0]+" :: "+service
    tpanel=paneljson()
    tpanel['id']=panidx
    tpanel['span']=spanl
    rid=0
    for server in hosts:
        target = panelstring(server,service,item)
        tpanel['targets'].append({"refId": refid[rid], "target": target })
        rid += 1
    tpanel['title']=pname
    base['dashboard']['rows'][row]['panels'].append(tpanel)
    panidx += 1
    return base

#Convert a string for grafana targets
def panelstring(host,service,item):
    s = "."
    seq = ("sensu", host, service, item)
    return s.join( seq )

#Get servers from argo
def getargo(environment, component):
    request_headers = {'Accept': 'application/json','Content-Type': 'application/json; charset=UTF-8'}
    url = 'https://argo.chronos.hcom/environment/'+environment+'/component/'+component+'/instances'
    http = httplib2.Http(disable_ssl_certificate_validation=True, timeout=120)
    resp, content = http.request(url, 'GET', '', request_headers)
    jsoncontent=json.loads(content)
    servers=[]
    for result in jsoncontent['instances']:
        shortname=result['value']['server'].split('.')[0]
        servers.append(shortname)
    return servers

def uploadgraph(data):
    global environment
    if environment == "prod":
        url = 'https://dashboard.prod.hcom/api/dashboards/db'
        headers = {'Accept': 'application/json','Content-Type': 'application/json','Authorization': 'Bearer eyJrIjoiTXVUc1BSS0UzWXBMdUQ4YklhNWttTmN0M0pNM0p5bmwiLCJuIjoidGVjaG9wcyIsImlkIjoxfQ=='}
    else:
        url = 'https://dashboard.lab.hcom/api/dashboards/db'
        headers = {'Accept': 'application/json','Content-Type': 'application/json','Authorization': 'Bearer eyJrIjoiakc2MEdQelhPQjBpRTQwSUo4bXZTandSa25ySkxmV2YiLCJuIjoidGVjaG9wcyIsImlkIjoxfQ=='}
    method='POST'
    body=json.dumps(data)
    http = httplib2.Http(disable_ssl_certificate_validation=True, timeout=120)
    resp, content = http.request( url, method, body, headers,)
    print content
    print resp
#Grafana Panel Template
def paneljson():
    panel=json.loads('{"aliasColors":{},"bars":false,"dashLength":10,"dashes":false,"datasource":null,"fill":1,"id":null,"legend":{"alignAsTable":true,"avg":false,"current":false,"max":false,"min":false,"rightSide":true,"show":true,"total":false,"values":false},"lines":true,"linewidth":1,"links":[],"spaceLength":10,"span":6,"stack":false,"steppedLine":false,"targets":[],"thresholds":[],"timeFrom":null,"timeShift":null,"title":"Disk :: % Used","tooltip":{"shared":true,"sort":0,"value_type":"individual"},"type":"graph","xaxis":{"buckets":null,"mode":"time","name":null,"show":true,"values":[]},"yaxes":[{"format":"short","label":null,"logBase":1,"max":"100","min":null,"show":true},{"format":"short","label":null,"logBase":1,"max":null,"min":null,"show":true}]}')
    return panel

#Granfana Basic Dashboard Template
def dashjson():
    dash=json.loads('{"dashboard":{"annotations":{"list":[]},"editable":true,"gnetId":null,"graphTooltip":0,"hideControls":false,"id":null,"links":[],"rows":[],"schemaVersion":14,"style":"dark","tabs":[],"templating":{"list":[]},"time":{"from":"now-6h","to":"now"},"timepicker":{"refresh_intervals":["5s","10s","30s","1m","5m","15m","30m","1h","2h","1d"],"time_options":["5m","15m","1h","6h","12h","24h","2d","7d","30d"]},"timezone":"browser","title":"bill_base_template","version":1},"overwrite":true}')
    return dash

#build the dashboard
def builddboard():
    global rowidx, environment, component
    gtype=fileopt()
    base=dashjson()
    if environment == "null":
        hosts=[component]
        gtype="single"
    else:
        hosts=getargo(environment,component)
    if gtype=="single":
        for item in hosts:
             servers=[]
             servers.append(item)
             base=board_one(base,servers)
    if gtype=="all":
        base=board_one(base,hosts)
    print json.dumps(base,indent=2,sort_keys=True)
    uploadgraph(base)


#boards
def board_one(base,servers):
    global rowidx,component
    base=rowadd(base)
    base=paneladd(base,rowidx-1,servers,"io","*",component,4)
    base=paneladd(base,rowidx-1,servers,"cpu","*",component,4)
    base=paneladd(base,rowidx-1,servers,"memory","*",component,4)

    base=rowadd(base)
    base=paneladd(base,rowidx-1,servers,"disk","*",component,4)
    base=paneladd(base,rowidx-1,servers,"netstat","*",component,4)
    base=paneladd(base,rowidx-1,servers,"netio","*",component,4)
    return base

#Main
builddboard()
