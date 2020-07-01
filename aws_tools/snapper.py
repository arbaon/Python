#! /usr/bin/python
import json
import subprocess
import time
from sys import argv
if len(argv) < 2:
    print "no arguments account id set to default"
    tag = "WEB"   
else:
    tag = argv[1]
#Define Functions
def datecheck( target ):
    FMT="%Y-%m-%d"
    result = ((time.mktime(time.strptime(today,FMT))) - (time.mktime(time.strptime(target,FMT)))) / 86400
    return result
#Define Variables
acc = 0
accounts=[{'id':'055143862093','acc':'clinical-skills','reg':'eu-west-1'}]
today=time.strftime("%Y-%m-%d")
snapshots=subprocess.check_output (["aws","ec2","describe-snapshots","--profile",accounts[acc]['acc'],"--owner-id",accounts[acc]['id'],"--region",accounts[acc]['reg']])
#Load json files
inst = json.load(open('instances.json'))    
data = json.loads(snapshots)
#Backup 
print 'Creating Snapshots'
y=0
while y < len(inst['Instances']):
    if tag == 'ALL' or tag in inst['Instances'][y]['Type']: 
        print ' aws ec2 create-snapshots --volume-id %s --description "SNAPPER %s %s" ' % (inst['Instances'][y]['VolId'],today,inst['Instances'][y]['Name'])
    y+=1
#Cleanup old Snapshots
print 'Removing Snapshots older than 14 days'
x = 0
while x < len(data['Snapshots']):
    if "NS" in data['Snapshots'][x]['Description']:
        stime = data['Snapshots'][x]['StartTime'].split('T')[0]
	myresult=int(datecheck( stime ))
	if myresult > 14:
	    print 'aws ec2 delete-snapshot --snapshot-id %s ' % (data['Snapshots'][x]['SnapshotId'])
    x+=1
