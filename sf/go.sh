#!/bin/bash

# defaults: http://linuxcommand.org/lc3_wss0120.php
if [ "$1" != "" ]; then
  inputfile=$1
else
  echo "[warn] no arg, defaulting to 'doc.html'"
  inputfile="doc.html"
fi

echo "[info] $inputfile being scanned"

# get Notice of Defaults and regex for their APNs
./nod2apn.py -i $inputfile -o nod_apn.txt
exit

# sort them, stackoverflow.com/questions/29244351
sort -o nod_apn.txt nod_apn.txt

# APN to Address & GPS coordinate
#https://dev.socrata.com/foundry/data.sfgov.org/45et-ht7c
#https://data.sfgov.org/resource/45et-ht7c.json?mapblklot=3624001
./apn2geo.py -i nod_apn.txt

# map addr.csv file
./map.R addr.csv map.pdf
