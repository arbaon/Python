#! /usr/bin/python
import json,re,subprocess,time
from sys import argv
#Define Functions
def datecheck( target ):
    FMT="%Y-%m-%d"
    result = ((time.mktime(time.strptime(today,FMT))) - (time.mktime(time.strptime(target,FMT)))) / 86400
    return result
#Define Variables
findaccid=subprocess.check_output(["aws","iam","get-user"])
tmpid=re.search('"Arn": "arn:aws:iam::(.+?):', findaccid)
if tmpid:
    accid=tmpid.group(1)
    today=time.strftime("%Y-%m-%d")
    snapshots=subprocess.check_output(["aws","ec2","describe-snapshots","--owner-id",accid])
    instances=subprocess.check_output(["aws","ec2","describe-instances","--filters","Name=instance-state-name,Values=running","Name=owner-id,Values="+accid])
    #Load json files
    inst = json.loads(instances)
    data = json.loads(snapshots)
    #Backup 
    print 'Creating Snapshots'
    y=0
    while y < len(inst['Reservations']):
	z=0
	while z < len(inst['Reservations'][y]['Instances'][0]['BlockDeviceMappings']):
	    if inst['Reservations'][y]['Instances'][0]['BlockDeviceMappings'][z]:
		Describe = inst['Reservations'][y]['Instances'][0]['Tags'][0]['Value']
		Volumeid = inst['Reservations'][y]['Instances'][0]['BlockDeviceMappings'][0]['Ebs']['VolumeId']
		Description = "SNAPPER "+today+" "+Describe
                print ' aws ec2 create-snapshot --volume-id %s --description "%s" ' % (Description)
		#subprocess.call(["aws","ec2","create-snapshot","--volume-id",Volumeid,"--description",Description])
            z+=1    
        y+=1
    #Cleanup old Snapshots
    print 'Removing Snapshots older than 14 days'
    x = 0
    while x < len(data['Snapshots']):
        if "SNAPPER" in data['Snapshots'][x]['Description']:
            stime = data['Snapshots'][x]['StartTime'].split('T')[0]
	    myresult=int(datecheck( stime ))
	    if myresult > 14:
		delsnap = data['Snapshots'][x]['SnapshotId']
	        print 'aws ec2 delete-snapshot --snapshot-id %s ' % (delsnap)
		#subprocess.check_output(["aws","ec2","delete-snapshot","--snapshot-id",delsnap])
        x+=1
else:
    print 'No Valid AWS Account ID Found'
