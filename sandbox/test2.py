import json
import os
import re
from itertools import chain

shared_stack_regexp = re.compile(r"^([a-z]+)")
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
def environment_arg():
    return "?environment=staging"
def merge_append(d, kv_list):
  map(lambda (k,v): d.setdefault(k, []).append(v), kv_list)
  return d
def host_group(g): return g + "/servers"

def b_group_and_hostgroup(group_name, instance_vars):
  return [ (group_name, instance_vars['instance_name']),
           (host_group(group_name), instance_vars['instance_host']),
           (host_group("all"), instance_vars['instance_host'])
         ]

inv_data = get_inventory_data()
dict_inventory = {
  "localhost": ["localhost"],
  "_meta": {
    "hostvars": { "localhost": { "ansible_python_interpreter": "/usr/bin/python2.6", "ansible_connection": "local" } }
  }
}
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
group_builders = [
  lambda i: [('__hostvars', (i['instance_name'], i))],  # special key to store instance and server hostvars
  lambda i: [('__hostvars', (i['instance_host'], server_hostvars(i)))],
  lambda i: b_group_and_hostgroup(i['instance_main_group'], i),
  lambda i: b_group_and_hostgroup(i['instance_stack'], i),
  lambda i: b_group_and_hostgroup(i['instance_component'], i),
  build_1st_and_rest
]
def inventory_keys(instance):
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
    "instance_main_group": instance['environment'] + "_" + instance['component']
  }
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
