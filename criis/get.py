#!/usr/bin/env python3
# https://realpython.com/run-python-scripts
import re
import urllib3
import datetime

### Globals
###########
url_set = set()
apn_set = set()
domain = '''http://www.criis.com'''

def getTime():
	return datetime.datetime.now().time()

# https://stackoverflow.com/questions/36516183/what-should-i-use-to-open-a-url-instead-of-urlopen-in-urllib3
# https://urllib3.readthedocs.io/en/latest/user-guide.html
def getData3(page):
	http = urllib3.PoolManager()
	r = http.request('GET', domain + page)
	return r.data.decode('utf-8')
	
def getData2(page):
	c = urllib2.urlopen(domain+url).read()
	#print('len(c)['+str(len(c))+']'+url) # concat str objects w/o spaces
	return c

### Main
##########

print('Begin Parse:', getTime())
filename = "doc.html"
data = open(filename, "r").read()		
# regex: findall pages that end with '_A'
m = re.findall('.*?href="(.*?_A).*?', data)
if m is None:
	raise SystemExit
# remove m's duplicate by creaitng set
pg_set = set(m)
print('End   Parse:', getTime())

# get data from each url and parse out APN
for pg in pg_set:
	c = getData3(pg)
	m = re.search('.*>([0-9]{4}-.*?)<.*', c)
	if m is not None:
		apn_set.add(m.group(1))
		#print "apn:", m.group(1)
	print('.', end='')

# output APNs
f = open('apn.txt', 'w')
for apn in apn_set:
	f.write(apn)
f.close()
print("apn.txt written:", len(apn_set))

