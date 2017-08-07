# -*- coding: utf-8 -*-

import googlemaps
import json
from mainDb import DB
import time

gmaps=googlemaps.Client(key='AIzaSyDxs7aecYhknVT_0_YVjvG1daFJpIjqLSg')

def returnLatLng(addr):
	geocode_result=gmaps.geocode(addr)
	res={'latitude':geocode_result[0]["geometry"]["location"]["lat"], 'longitude':geocode_result[0]["geometry"]["location"]["lng"]}
	return res

db=DB('ini/connect.ini')
db.connect()
SelectResult=db.executeQuery('SELECT id, address FROM branches WHERE latitude_longitude IS NULL AND id>2 LIMIT 2500', 1)
i=0
for res in SelectResult:
#cose query may return multiple colls, it's neccessary call only first coll with address
	i=i+1
	if(i==10):
		time.sleep(1)
		i=0
	lat_lng=returnLatLng(res[1])
	db.executeQuery('UPDATE branches SET latitude_longitude=GeomFromText("POINT(%s %s)") WHERE id=%s'%(lat_lng['latitude'], lat_lng['longitude'], res[0]), 2)

db.closeConnection()

