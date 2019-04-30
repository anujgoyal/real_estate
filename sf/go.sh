#!/bin/bash

# get Notice of Defaults and regex for their APNs
./get.py -i nod_apr19.html 

# sort them, stackoverflow.com/questions/29244351
sort -o apn.txt apn.txt

# get addresses of each APN
./ref.py

#https://dev.socrata.com/foundry/data.sfgov.org/45et-ht7c
#https://data.sfgov.org/resource/45et-ht7c.json?mapblklot=3624001
