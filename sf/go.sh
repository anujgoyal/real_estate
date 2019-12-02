#!/bin/bash

# defaults: http://linuxcommand.org/lc3_wss0120.php
# if a file is passed in parse it
if [ "$1" != "" ]; then
  inputfile=$1
# otherwise run node/puppeteer to get nod.html 
else
  node criis.js >nod.html
  inputfile=nod.html
fi

echo "[info] $inputfile being scanned"

# get Notice of Defaults and regex for their APNs
./nod2apn.py -i $inputfile -o nod_apn.txt

# sort them, stackoverflow.com/questions/29244351
#sort -o nod_apn.txt nod_apn.txt

# merge the apn and date
./merge.py -i nod_apn.txt -o n.csv

# APN to Address & GPS coordinate
#https://dev.socrata.com/foundry/data.sfgov.org/45et-ht7c
#https://data.sfgov.org/resource/45et-ht7c.json?mapblklot=3624001
./apn2geo.py -i n.csv -o addr.csv

# map addr.csv file
./map.R addr.csv map.pdf
