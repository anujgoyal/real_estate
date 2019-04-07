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
import csv

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
		c = d[1]['geometry']['coordinates'] # coordinate list
		pt = c[0][0] # first coordinate
		#print(apn,",",a['from_st']," ",a['street'],",",pt[0],",",pt[1], sep='') #a['st_type'])
		s = (apn,a['from_st']+" "+a['street'],pt[0],pt[1])
		print('.', end='', flush=True) #print(s)
		return s

#print('Begin Parse:', getTime())
#getAddy("3624001")
#getAddy("3624002")
#getAddy("0282-022")
#print('End   Parse:', getTime())

print('Begin Parse:', getTime())
apns = open('apn.txt', "r").read().splitlines()
addyList = []
for apn in apns:
	a = getAddy(apn)
	addyList.append(a)
print('\nEnd   Parse:', getTime())
 
# output addresses
# https://stackoverflow.com/questions/15578331/save-list-of-ordered-tuples-as-csv
with open('addr.csv', 'w') as f:
	fw = csv.writer(f) #fw: file writer
	fw.writerow(['apn','addy','long','lat'])
	for addy in addyList:
		fw.writerow(addy)
f.close()	
print("\naddr.csv written:", len(addyList))

sys.exit()

# https://thefrontsteps.com/2016/08/01/bay-area-liquefaction-landslide-and-seismic-zones-mapped/
# http://urbanspatialanalysis.com/dataviz-tutorial-mapping-san-francisco-home-prices-using-r/
# http://simonkassel.com/blog/2017/2/21/mapping-and-visualizing-san-franciscos-residential-real-estate-market-with-r
# https://www.arcgis.com/home/item.html?id=2d5b69b44e4c4f1b90bafcae9b823c17
