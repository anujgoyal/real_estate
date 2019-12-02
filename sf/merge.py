#!/usr/bin/env python3
import csv
import datetime
import getopt
import pandas as pd 
import re
import sys

#print("print: pp")
#sys.stdout.write("out: ww\n")
#sys.stderr.write("err: ee\n")

### MERGE
#########
# https://www.geeksforgeeks.org/python-pandas-dataframe-groupby/
# https://pandas.pydata.org/pandas-docs/stable/reference/frame.html
# https://www.shanelynn.ie/using-pandas-dataframe-creating-editing-viewing-data-in-python/
# https://stackoverflow.com/questions/59123853/python3-how-to-print-groupby-last/59124094#59124094
def merge(ifile,ofile):
	df = pd.read_csv(ifile)
	g = df.groupby('apn').last()
	g.to_csv(ofile)

### MAIN
########
def main(argv):
	inputfile = 'n2.txt'
	outputfile = 'n2.csv' # this is just for testing

	#https://docs.python.org/2/library/getopt.html
	try:
		opts,args = getopt.getopt(argv, "hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print('usage: merge.py -i <inputfile>')
		sys.exit(1)

	for opt, arg in opts:
		if opt=='h':
				print('usage: merge.py -i <inputfile>')
				sys.exit()
		elif opt in ("-i", "--ifile"):
				inputfile = arg
				print('[merge] inputfile: ', inputfile)
		elif opt in ("-o", "--ofile"):
				outputfile = arg
				print('[merge] outputfile: ', outputfile)

	# do stuff
	merge(inputfile, outputfile)
	sys.exit()

if __name__== "__main__":
	main(sys.argv[1:])
