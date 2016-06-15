#!/usr/bin/python

import urllib2
import json
import config

FILE_NAME = 'external_ip.txt'
API_KEY = config.key('IFTTT_EXTERNAL_IP_CHANGED_KEY')
IFTTT_URL = 'https://maker.ifttt.com/trigger/external_ip_changed/with/key/{}'.format(API_KEY)

with open(FILE_NAME, "r+") as f:
    old_external_ip = f.read()
    current_external_ip = urllib2.urlopen('https://api.ipify.org/?format=text').read()
    print "Current external IP address={}".format(current_external_ip)
    f.seek(0)
    f.write(current_external_ip)
    f.truncate()
    if old_external_ip != current_external_ip:
        print "New external IP address ({}) differs from old external IP address ({})".format(current_external_ip, old_external_ip)
        data = json.dumps({'value1':current_external_ip})
        print "will send data to ifttt: {}".format(data)
        req = urllib2.Request(IFTTT_URL, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
    else:
        print "IP address has not changed since last check."
    f.close()
