#!/usr/bin/env python

import json
import requests
from pprint import pprint
# Netbox URL
URL = 'http://35.198.136.252:32768'

# Netbox API Token
TOKEN = '126262c5b9c13a7a1102ee1e1a416004f5bf8217'

headers = {  
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Token ' + TOKEN
}
# Netbox app's

DEVICES = '/api/dcim/devices'



def get_dcim_devices():
    dcim_devices = requests.get(URL + DEVICES, headers = headers).json()
    return dcim_devices


if __name__ == "__main__":

    devices = []
    inventory = {}
    hostvars = {}
    all_hosts = {}

    output = get_dcim_devices()
    if isinstance(output, dict) and "results" in output:
        devices += output['results']

        for i in devices:
            if i['primary_ip']:
                hostvars.setdefault('_meta', {'hostvars': {}})['hostvars'][i['name']] = {"ansible_host": str(i['primary_ip']['address']).split("/", 1)[0]}
            else:
                hostvars.setdefault('_meta', {'hostvars': {}})['hostvars'][i['name']] = {"ansible_host": {}}
            if i['config_context']:
                hostvars['_meta']['hostvars'][i['name']].update(i['config_context'])
            if i ['name']:
                all_hosts.setdefault('all', {'hosts': []})['hosts'].append(i['name'])

inventory.update(hostvars)
inventory.update(all_hosts)
print(json.dumps(inventory, indent=4))