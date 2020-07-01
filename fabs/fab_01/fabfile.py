from __future__ import with_statement
from fabric.api import *
myout=[]
env.hosts = open('../../inv/last_milan', 'r').readlines()
env.user = 'bcorbett'
env.output_prefix = False

def deploy(tag, force=False):
    with settings(warn_only=True):
        script_f = open('../../scripts/yumhistory.sh')
        #tmp=sudo(script_f.read())
        tmp=sudo("yum history info $(yum history | grep bcorbet | cut -d'|' -f5 | awk '{print $1}') | grep 'Return-Code'")
        myout.append(tmp)
        post_deploy()
def post_deploy():
    print("\n".join(myout))
