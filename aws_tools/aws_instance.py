#!/usr/bin/python
import json
import subprocess
import time
snapshots=subprocess.check_output (["aws","ec2","describe-instances","--profile","clinical-skills"])

print snapshots
data = json.loads(snapshots)
x =0
while x < len(data['Reservations']):
    print "Instance Name: %s" % (data['Reservations'][x]['Instances'][0]['Tags'][0]['Value'])
    print "Instance ID: %s" % (data['Reservations'][x]['Instances'][0]['InstanceId'])
    print "Volume ID: %s" % (data['Reservations'][x]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId'])
    print
    x+=1
