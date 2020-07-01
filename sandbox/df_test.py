#!/usr/bin/env python

import re
import os
import json
import os.path
import time
import sys
import getpass
from itertools import chain

shared_stack_regexp = re.compile(r"^([a-z]+)")
script_path = os.path.abspath(sys.argv[0]) # save it ASAP before some random code changes current dir

_env_debug = { 'value': None, 'source': None }

def environment_arg():
    """
    Filter Argo output about specific environment only. Detect one we want to use
    with following precedence rules (first match wins):
      - deploy_environment variable
      - inventory script file  name if differs from 'argo.py'
      - parent directory of inventory script if grandparent starts with "inventor*" 
        (this is most shady and error prone)
      - return error otherwise, in new world we force argo envs to be filtered
    """
    
    def fmt(env, src): # helper func to format arg and set _env_debug
       f = "?environment=%s"
       _env_debug['value'] = env
       _env_debug['src'] = src
       return f % (env,)

    if os.getenv("deploy_environment"):  # use env var if set
      return fmt(os.getenv("deploy_environment"), 'environment var') 

    me = os.path.basename(script_path)
    if me != "argo.py":
      return fmt(me.split('.')[0], 'script filename')  # use filename up to first '.'

    parent = os.path.dirname(script_path)
    grandparent = os.path.dirname(parent)

    if os.path.basename(grandparent).startswith("inventor"):
      return fmt(os.path.basename(parent), 'script parent dir') # use inventory directory name

    # can't detect env to use, erroring
    sys.stderr.write(
""" 
    [ERROR] Argo inventory script is unable to detect environment you are trying to use.
    Please do one (not ALL!) of following, loosely ordered by preference:

     - Make an env inventory dir inside 'inventories' dir and symlink argo.py in there:
        `mkdir -p inventories/myenv; ln -s ../../argo.py inventories/myenv/;`
       As a bonus you can have env-specific group_vars

     - Make a symlink from argo.py to a file named after env you want to use:
        `ln -s argo.py myenv.py`

     - set deploy_environment environment variable to Argo env you want to use
"""
    )
    sys.exit(1)


def query_argo():
    import httplib2

    try:
        from urlparse import urlparse
    except ImportError:
        from urllib.parse import urlparse

    request_headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json; charset=UTF-8'
    }

    env_url = os.getenv('argo', 'https://argo.chronos.hcom')
    url = env_url + '/inventory' + environment_arg()

    target = urlparse(url)

    # ORIGINAL line where ssl cert was not ignored - refer to DEVINF-488
    #http = httplib2.Http()
    http = httplib2.Http(disable_ssl_certificate_validation=True, timeout=120)
  
    response, content = http.request(target.geturl(), 'GET', '', request_headers)

    return content

def get_inventory_data():
    return json.loads(query_argo())

inv_data = get_inventory_data()

dict_inventory = {
  "localhost": ["localhost"],
  "_meta": {
    "hostvars": { "localhost": { "ansible_python_interpreter": "/usr/bin/python2.6", "ansible_connection": "local" } }
  }
}


# [(k1,v1),(k1,v2)] -> {k1: [v1, v2]}
def merge_append(d, kv_list):
  map(lambda (k,v): d.setdefault(k, []).append(v), kv_list)
  return d

def host_group(g): return g + "/servers"

def b_group_and_hostgroup(group_name, instance_vars): 
  return [ (group_name, instance_vars['instance_name']),
           (host_group(group_name), instance_vars['instance_host']),
           (host_group("all"), instance_vars['instance_host'])
         ]

def build_1st_and_rest(instance_vars):
  if instance_vars['instance_name'].endswith('-01'): 
    return b_group_and_hostgroup("1st_instances", instance_vars)

  res = b_group_and_hostgroup("rest_instances", instance_vars)

  instance_name_parts = instance_vars['instance_name'].split('-')
  if "pipeline" not in instance_vars['instance_name'] and len(instance_name_parts) == 3:
    if int(instance_name_parts[2]) % 2:
      res.extend(b_group_and_hostgroup("rest_odd_instances", instance_vars))
    else:
      res.extend(b_group_and_hostgroup("rest_even_instances", instance_vars))
  return res

def server_hostvars(i):
  return {
     "server_stack": i["instance_stack"],
     "server_shared_stack": i["instance_shared_stack"]
  }

# all builders are:  instance_vars -> [(groupname, instance_name), ....]
group_builders = [
  lambda i: [('__hostvars', (i['instance_name'], i))],  # special key to store instance and server hostvars
  lambda i: [('__hostvars', (i['instance_host'], server_hostvars(i)))],
  lambda i: b_group_and_hostgroup(i['instance_main_group'], i),
  lambda i: b_group_and_hostgroup(i['instance_stack'], i),
  lambda i: b_group_and_hostgroup(i['instance_component'], i),
  build_1st_and_rest
]


def inventory_keys(instance):
  username = getpass.getuser()
  proxy_one = '\'-o ProxyCommand="ssh -W %h:%p -q '
  instance_vars = {
    "ansible_ssh_host": instance['server'],
    "instance_host": instance['server'],
    "instance_stack": instance['environment'],
    "instance_shared_stack": shared_stack_regexp.match(instance['environment']).groups()[0],
    "instance_type": instance['component'],
    "instance_component": instance['component'],
    "instance_path": instance['basepath'],
    "instance_name": instance['instance'],
    "instance_realname": instance['instance'],
    "instance_main_group": instance['environment'] + "_" + instance['component'],
  }
  if 'scrappy' in instance['metadata']:
    instance_vars.update({"ansible_ssh_common_args" : proxy_one + username + "@" + instance['metadata']['scrappy'] + "\"'"})

  return chain.from_iterable(b(instance_vars) for b in group_builders)

inventory = reduce(merge_append, map(inventory_keys, inv_data['instances']), dict_inventory)

inventory["_meta"].setdefault("hostvars", {}).update(dict((name, hv) for (name, hv) in inventory.get("__hostvars",{})))
if "__hostvars" in inventory: 
  del inventory["__hostvars"]
else:
  sys.stderr.write(
"""
  [WARNING] Argo inventory returned no instances, I was using environment '%(value)s' inferred from '%(src)s'

""" % _env_debug)

print json.dumps(inventory, sort_keys=True, indent=4, separators=(',', ': '))
