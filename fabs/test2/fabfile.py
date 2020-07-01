from __future__ import with_statement
from fabric.api import *
myout=[]
env.hosts = open('hosts_file', 'r').readlines()
env.user = 'bcorbett'
env.output_prefix = False

def deploy(tag, force=False):
    with settings(warn_only=True):
	script_f = open('test_script.sh')
	tmp=run(script_f.read())
	myout.append(tmp)
    post_deploy()
def post_deploy():
    print("\n".join(myout))
