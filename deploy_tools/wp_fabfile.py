from __future__ import with_statement
from fabric.api import *

env.roledefs = {
    'web': ['52.58.94.149']
}

env.user = 'ubuntu'
wp_dir = '/srv/sites/<put name here>'
git_dir = '/srv/sites/<put name here>'
repo_url = 'git@bitbucket.org:nameofrepo.git'

@roles('web')
def deploy(tag, force=False):
    """
    Comments go here.
    """
    with settings(warn_only=true):
	if run("test -d %s" % git_dir).failed
	    run("git clone %s %s" % (repo_url, git_dir))
    with cd(git_dir):
	pull_result = run('git pull origin %s' % tag)
        """ Only perform deployment tasks if repo was updated """
        if "up-to-date" not in pull_result or force:
            run("git checkout %s" % tag)
    post_deploy()
def sync_data():
    sudo("rsync -av %s/wp-content/themes/elsevier/ %s/wp-content/themes/elsevier/" % (git_dir, wp_dir))
    sudo("chown -R centos.nginx %s" % wp_dir)
def restart_services(program='nginx'):
    """
    Restarts nginx via supervisorctl
    """
    sudo("supervisorctl restart %s:" % program)
def post_deploy():
    """
    Run all cleanup and post-deployment operations like restarting services
    """
    sync_data()
    restart_services()
