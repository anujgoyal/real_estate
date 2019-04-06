#!/usr/bin/env python3
# https://realpython.com/run-python-scripts
# https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
import re
import certifi 
import urllib3
import datetime
#import json
import rapidjson
import sys

## Global
#url = "https://data.sfgov.org/resource/45et-ht7c.json?mapblklot=" 
# after trial and error determined that blklot better than mapblklot
url = "https://data.sfgov.org/resource/45et-ht7c.json?blklot=" 
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

## getTime
def getTime():
	return datetime.datetime.now().time()

## getAddy
def getAddy(apn):
		apn = apn.replace("-","")
		r = http.request('GET', url + apn)
		data = r.data.decode('utf-8')
		d = rapidjson.loads(data)
		if len(d) < 1:
			print(apn, ",NA", sep='')
			return
		a = d[0] #address info
		#print(apn,",",a['from_st'], a['street'], a['st_type'])
		print(apn,",",a['from_st'], a['street'])

#print('Begin Parse:', getTime())
#getAddy("3624001")
#getAddy("3624002")
#getAddy("0282-022")
#print('End   Parse:', getTime())

print('Begin Parse:', getTime())
apns = open('apn.txt', "r").read().splitlines()
for apn in apns:
	getAddy(apn)
print('End   Parse:', getTime())
 
# output addresses
#f = open('addy.txt', 'w')
#for apn in apn_set:
#	f.write(apn)
#	f.write('\n')
#f.close()
#print("\napn.txt written:", len(apn_set))

sys.exit()
