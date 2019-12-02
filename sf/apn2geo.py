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
http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
# after trial and error determined that blklot better than mapblklot
#url = "https://data.sfgov.org/resource/45et-ht7c.json?mapblklot=" 
#url = "https://data.sfgov.org/resource/45et-ht7c.json?blklot=" 
# 2019.09.24
# https://data.sfgov.org/Geographic-Locations-and-Boundaries/-Deprecated-Addresses-with-Units-Enterprise-Addres/dxjs-vqsy
# https://data.sfgov.org/Geographic-Locations-and-Boundaries/Addresses-with-Units-Enterprise-Addressing-System/ramy-di5m
# https://dev.socrata.com/foundry/data.sfgov.org/ramy-di5m
url = "https://data.sfgov.org/resource/ramy-di5m.json?parcel_number="
# [{  'eas_baseid': '283633', 
#      'eas_subid': '493314',
#     'eas_fullid': '283633-493314-316890',
#        'address': '2701 VAN NESS AVE #603',
#    'unit_number': '603',
# 'address_number': '2701',
#    'street_name': 'VAN NESS',
#    'street_type': 'AVE',
#  'parcel_number': '0503081',
#          'block': '0503',
#            'lot': '081',
#            'cnn': '13169101',
#      'longitude': '-122.42484884',
#       'latitude': '37.80057332',
#       'zip_code': '94123',
#          'point': {'type': 'Point', 'coordinates': [-122.4248488368, 37.8005733222]},
#        'supdist': 'SUPERVISORIAL DISTRICT 3',
#     'supervisor': '3',
#     'supdistpad': '03',
#     'numbertext': 'THREE',
#        'supname': 'Peskin',
#          'nhood': 'Russian Hill'}]

def getAddy(apnDate):
	apn = apnDate.apn
	date = apnDate.date
	apn = apn.replace("-","")         # cleanup apn by removing dashes
	r = http.request('GET', url+apn)  # make http call and assign response
	data = r.data.decode('utf-8')     # pull data out of response
	j = rapidjson.loads(data)         # convert data to json dictionary

	# sometimes there is no data, so write 'apn, NA, 0, 0'
	if len(j) < 1:
		s = (apn,"NA",0,0)
		print("[getaddy]",apn,"->","not found")
	# if data, get dict
	else:
		d = j[0]
		addr = d['address']
		lon  = d['longitude']
		lat  = d['latitude']
		#debug: print(apn,",",a['from_st']," ",a['street'],",",pt[0],",",pt[1], sep='') #a['st_type'])
		s = (apn,date,addr,lon,lat)
		print("[getaddy]",apn,",",date,"->",addr)
	return s

# DEBUGGING
#getAddy("3624001")
#getAddy("3624002")
#getAddy("0282-022")

def getTime():
	return datetime.datetime.now().time()

class ApnDate:
  def __init__(self, apn, date):
    self.apn = apn
    self.date = date

# read APNs from inputfile
def readfile(filename):
	#apns = open(filename, "r").read().splitlines()
	#return apns
	apnList = []
	reader = rd = csv.DictReader(open(filename))
	for r in reader:
		ad = ApnDate(r['apn'], r['date'])
		apnList.append(ad)
	return apnList

# get addresses
def getAddresses(apnList):
	print('[apn2geo] begin:', getTime())
	addyList = []
	for ad in apnList:
		try:
			txt = getAddy(ad)
			addyList.append(txt)
		except:
			print("[error] getting address from apn:", apn)
	print('[apn2geo] end:', getTime())
	return addyList

# write file
def writefile(filename, addyList):
	# https://stackoverflow.com/questions/15578331/save-list-of-ordered-tuples-as-csv
	with open(filename, 'w') as f:
		fw = csv.writer(f) #fw: file writer
		fw.writerow(['apn','addy','long','lat'])
		for addy in addyList:
			fw.writerow(addy)
		f.close()	
		print("[apn2geo]", filename, "written:", len(addyList))

### Main
##########
def main(argv):
	inputfile = ''
	outputfile = 'addr.csv' # default

	#https://docs.python.org/2/library/getopt.html
	try:
		opts,args = getopt.getopt(argv, "hi:o:g:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('usage: ./apn2geo.py -i <inputfile>')
		sys.exit(1)

	for opt, arg in opts:
		if opt=='h':
			print('usage: ./apn2geo.py -i <inputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg
			print('[apn2geo] inputfile: ', inputfile)
		elif opt in ("-o", "--ofile"):
			outputfile = arg
			print('[apn2geo] outputfile: ', outputfile)
		elif opt in ("-g"):
			apn = arg
			print('[apn2geo] apn: ', apn)
			getAddy(apn)
			sys.exit() 	

	# do work
	apnList = readfile(inputfile)
	addyList = getAddresses(apnList)
	writefile(outputfile, addyList)
	sys.exit()

if __name__== "__main__":
        main(sys.argv[1:])

