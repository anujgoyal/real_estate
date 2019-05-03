#!/usr/bin/env python3
################################################################################ 
# this program takes a list of APNs and outputs a CSV file
# the CSV file format is: APN, Address, Latitude, Longitude
################################################################################ 
# https://realpython.com/run-python-scripts
# https://urllib3.readthedocs.io/en/latest/user-guide.html#ssl
# https://thefrontsteps.com/2016/08/01/bay-area-liquefaction-landslide-and-seismic-zones-mapped/
# http://urbanspatialanalysis.com/dataviz-tutorial-mapping-san-francisco-home-prices-using-r/
# http://simonkassel.com/blog/2017/2/21/mapping-and-visualizing-san-franciscos-residential-real-estate-market-with-r
# https://www.arcgis.com/home/item.html?id=2d5b69b44e4c4f1b90bafcae9b823c17
# https://www.littlemissdata.com/blog/maps
import re
import certifi 
import urllib3
import datetime
import rapidjson
#import json
import sys
import csv
import getopt

## Global
# after trial and error determined that blklot better than mapblklot
# url = "https://data.sfgov.org/resource/45et-ht7c.json?mapblklot=" 
url = "https://data.sfgov.org/resource/45et-ht7c.json?blklot=" 
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


def getTime():
	return datetime.datetime.now().time()

def getAddy(apn):
	# cleanup apn by removing dashes
	apn = apn.replace("-","")
	# make http call and assign response
	r = http.request('GET', url + apn)
	# pull data out of response
	data = r.data.decode('utf-8')
	# convert data to json dictionary
	d = rapidjson.loads(data)
	# sometimes there is no data, so write 'apn, NA, 0, 0'
	if len(d) < 1:
		print("\n", apn, ",NA", sep='')
		s = (apn,"NA",0,0)
		return s

	# otherwise there's data
	a = d[0] #address info
	c = d[1]['geometry']['coordinates'] # coordinate list
	pt = c[0][0] # first coordinate
	#debug: print(apn,",",a['from_st']," ",a['street'],",",pt[0],",",pt[1], sep='') #a['st_type'])
	if 'from_st' in a:
		s = (apn,a['from_st']+" "+a['street'],pt[0],pt[1])
		print('.', end='', flush=True) #print(s)
	else:
		s = (apn,"NA",0,0)
	return s

# DEBUGGING
#getAddy("3624001")
#getAddy("3624002")
#getAddy("0282-022")

def readfile(filename):
	# read APNs from inputfile
	print('APN2GEO BEG:', getTime())
	apns = open(filename, "r").read().splitlines()
	addyList = []
	for apn in apns:
		a = getAddy(apn)
		addyList.append(a)
	print('\nAPN2GEO END:', getTime())
	return addyList

def writefile(filename, addyList):
	# https://stackoverflow.com/questions/15578331/save-list-of-ordered-tuples-as-csv
	with open(filename, 'w') as f:
		fw = csv.writer(f) #fw: file writer
		fw.writerow(['apn','addy','long','lat'])
		for addy in addyList:
			fw.writerow(addy)
		f.close()	
		print("\naddr.csv written:", len(addyList))

### Main
##########
def main(argv):
	inputfile = ''
	outputfile = 'addr.csv' # default
	try:
		opts,args = getopt.getopt(argv, "hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('apn2geo.py -i <inputfile>')
		sys.exit(1)

	for opt, arg in opts:
		if opt=='h':
			print('usage: apn2geo.py -i <inputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
			print('inputfile: ', inputfile)
		elif opt in ("-o", "--ofile"):
			outputfile = arg
			print('outputfile: ', outputfile)

	# do work
	addyList = readfile(inputfile)
	writefile(outputfile, addyList)
	sys.exit()

if __name__== "__main__":
        main(sys.argv[1:])

