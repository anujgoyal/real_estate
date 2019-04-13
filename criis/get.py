#!/usr/bin/env python3
# https://realpython.com/run-python-scripts
import re
import urllib3
import datetime

### Globals
###########
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

# open file and regex out the URLs
# those URLs will later be opened to get the APNs
def getPages(filename):
	print('Begin Parse:', getTime())
	data = open(filename, "r").read()		
	m = re.findall('.*?href="(.*?_A).*?', data) # regex: findall pages that end with '_A'
	if m is None:
		raise SystemExit
	pg_set = set(m) # remove m's duplicate by creaitng set
	print('End   Parse:', getTime())
	return pg_set

# get data from each url and parse out APN
def getAPNs(pg_set):
	print('getAPNs:', len(pg_set))
	apn_set = set()
	for pg in pg_set:
		c = getData3(pg)
		m = re.search('.*>([0-9]{4}-.*?)<.*', c)
		if m is not None:
			apn_set.add(m.group(1)) #print "apn:", m.group(1)
		print('.', end='', flush=True)
	return apn_set

# write APNs
def writeAPNs(apn_set):
	f = open('apn.txt', 'w')
	for apn in apn_set:
		f.write(apn)
		f.write('\n')
	f.close()
	print("\nwriteAPNs:", len(apn_set))

### Main
### https://www.guru99.com/learn-python-main-function-with-examples-understand-main.html
##########
def main():
	pg_set = getPages("nod_apr19.html")
	apn_set = getAPNs(pg_set)
	writeAPNs(apn_set)
  
if __name__== "__main__":
	main()

