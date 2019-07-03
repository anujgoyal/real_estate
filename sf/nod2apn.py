#!/usr/bin/env python3
# https://realpython.com/run-python-scripts
import re
import urllib3
import datetime
import sys
import getopt

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

# for python2	
#def getData2(page):
#	return urllib2.urlopen(domain+url).read()

# open file and regex out the URLs
# those URLs will later be opened to get the APNs
def getPages(filename):
	print('Begin Parse:', getTime())
	data = open(filename, "r").read()		
	m = re.findall('.*?href="(.*?_A).*?', data) # regex: findall pages that end with '_A'
	if m is None:
		raise SystemExit
	pg_set = set(m) # remove m's duplicate by creating set
	print('End   Parse:', getTime())
	return pg_set

# get data from each url and parse out APN
def getAPNs(pg_set):
	print('getAPNs:', len(pg_set))
	apn = ''
	rdate = ''
	apn_set = set()
	for pg in pg_set:
		# open url and get c=contents
		c = getData3(pg)
		# search for APN
		m = re.search('.*>([0-9]{4}-.*?)<.*', c)
		if m is not None:
			apn = m.group(1)
			apn_set.add(apn) #print('apn: ', apn)
		# search for record date
		# <td colspan="2"><font face="Arial, Helvetica">05/24/2019</font></td>
		m = re.search('.*>([0-9]{2}/[0-9]{2}/[0-9]{4})<.*', c)
		if m is not None:
			rdate = m.group(1)
			print(apn+','+rdate)
		print('.', end='', flush=True)
	return apn_set

# write APNs
def writeAPNs(apn_set, filename):
	f = open(filename, 'w')
	for apn in apn_set:
		f.write(apn)
		f.write('\n')
	f.close()
	print("\nwriteAPNs:", len(apn_set))

### Main
### https://www.guru99.com/learn-python-main-function-with-examples-understand-main.html
##########
def main(argv):
	inputfile = ''
	outputfile = ''
	try:
		opts,args = getopt.getopt(argv, "hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('nod2apn.py -i <inputfile>')
		sys.exit(1)

	for opt, arg in opts:
		if opt=='h':
			print('nod2apn.py -i <inputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
			print('inputfile: ', inputfile)
		elif opt in ("-o", "--ofile"):
			outputfile = arg
			print('outputfile: ', outputfile)

    # do real work
	pg_set = getPages(inputfile)
	apn_set = getAPNs(pg_set)
	writeAPNs(apn_set, outputfile)
  
if __name__== "__main__":
	main(sys.argv[1:])

