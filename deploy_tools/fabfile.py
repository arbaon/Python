from __future__ import with_statement
from fabric.api import *

env.roledefs = {
    'web': ['52.58.94.149']
}

env.user = 'centos'
code_dir = '/srv/sites/qr.elsevier.de'
clone_dir = '/srv/clone/qr.elsevier.de'
repo_url = 'git@bitbucket.org:elsevieremea-ondemand/de-admintools.git'

@roles('web')
def deploy(tag, force=False):
    """
    Comments go here.
    """
    with settings(warn_only=true):
	if run("test -d %s" % clone_dir).failed
	    run("git clone %s %s" % (repo_url, clone_dir))
    with cd(clone_dir):
	pull_result = run('git pull origin %s' % tag)
        """ Only perform deployment tasks if repo was updated """
        if "up-to-date" not in pull_result or force:
            run("git checkout %s" % tag)
	    sudo('rm -rf "%s"' % code_dir)
            sudo("ln -s %s %s" % (clone_dir, code_dir))
    post_deploy()
def update_permissions()
    sudo("chown -R centos.nginx %s" % code_dir)
    sudo("chmod -R 755 %s" % code_dir)
    sudo ("find %s -type f -exec chmod 664 {} \;" % code_dir)
def restart_services(service1='nginx',service2='php-fpm'):
    """
    Restarts nginx via supervisorctl
    """
    sudo("supervisorctl restart %s:" % service1)
    sudo("systemctl restart %s:" % service2)
def post_deploy():
    """
    Run all cleanup and post-deployment operations like restarting services
    """
    update_permissions()
    restart_services()
