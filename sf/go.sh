#!/bin/bash

# get Notice of Defaults and regex for their APNs
./nod2apn.py -i nod_apr19.html 

# sort them, stackoverflow.com/questions/29244351
sort -o apn.txt apn.txt

# APN to Address & GPS coordinate
#https://dev.socrata.com/foundry/data.sfgov.org/45et-ht7c
#https://data.sfgov.org/resource/45et-ht7c.json?mapblklot=3624001
./apn2geo.py

# 

