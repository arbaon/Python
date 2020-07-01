from __future__ import with_statement
from fabric.api import *
env.hosts = open('hosts_file', 'r').readlines()
env.user = 'bcorbett'
env.output_prefix = False
def deploy(tag, force=False):
    with settings(warn_only=True):
	run("uname -a")
    post_deploy()
def post_deploy():
    """
    Run all cleanup and post-deployment operations like restarting services
    """
