# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import serial
import time
from pynmea import nmea
from django.shortcuts import render
import string
import math
from loki import loki
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def location(request):
	if request.method == 'POST':
		bound_lat = request.POST.get('bound_lat')
		bound_lon = request.POST.get('bound_lon')
		bound_radius = request.POST.get('bound_radius')
		data = loki(bound_lat, bound_lon, bound_radius)
		return HttpResponse(data)
		#Calculating Distance between current coords and boundary

def location2(request):
	port = serial.Serial("/dev/ttyAMA0",9600, timeout=3.0)
	gpgga = nmea.GPGGA()
	gprmc = nmea.GPRMC()
	while True:
		rcvd = port.readline()
		if rcvd[0:6] == '$GPRMC':
			gprmc.parse(rcvd)
			if gprmc.data_validity == 'V':
				print "No Location Found" + str(rcvd)

			else: 
				gprmc.parse(rcvd)
				latitude = gprmc.lat
				try:
					latitude = float(latitude)
				except ValueError:
					print "Lat Value Error" + latitude
				lat_direction = gprmc.lat_dir
				try:
					longitude = float(gprmc.lon)
				except ValueError:
					print "Longitude Value Error" + longitude
				lon_direction = gprmc.lon_dir

			
				gps_time = float(gprmc.timestamp)
				gps_hour = int(gps_time/10000.0)
				gps_min = gps_time%10000.0
				gps_sec = gps_min%100.0
				gps_min = int(gps_min/100.0)
				gps_sec = int(gps_sec)

				lat_deg = int(latitude/100.0) 
				lat_min = latitude - (lat_deg*100)
				lat_dec_deg = lat_deg + (lat_min/60)
			
				lon_deg = int(longitude/100.0)
				lon_min = longitude - (lon_deg*100)
				lon_dec_deg = lon_deg + (lon_min/60)
				lon_sec = lon_min%100.0
				lon_min = int(lon_min/100.0)

				print "Time: "+str(gps_hour)+":"+str(gps_min)+":"+str(gps_sec)
				print "Latitude: " + str(lat_dec_deg) + str(lat_direction)
				print "Longitude: " + str(lon_dec_deg) + str(lon_direction)
		elif rcvd[0:6] == '$GPGGA':
			gpgga.parse(rcvd)
			print rcvd



	
			
			
		
def location3(request):
	port = serial.Serial("/dev/ttyAMA0",9600, timeout=3.0)
	while True:
		rcvd = port.read(1200)
		pos1 = rcvd.find("$GPRMC")
		pos2 = rcvd.find("\n",pos1)
		loc = rcvd[pos1:pos2]
		data = loc.split(',')
		pos11 = rcvd.find("$GPGGA")
		pos22 = rcvd.find("\n", pos11)
		loc1 = rcvd[pos11:pos22]
		data1 = loc.split(',')
		if data[2] == 'V':
			print 'No location found'

		else:
			gps_time = float(data[1])
			gps_date = float(data[9])
			gps_hour = int(gps_time/10000.0)
			gps_min = gps_time%10000.0
			gps_sec = gps_min%100.0
			gps_min = int(gps_min/100.0)
			gps_sec = int(gps_sec)

			print "latitude = "+data[3]+data[4]
			print "longitude = "+data[5]+data[6]
			print "time=",gps_hour,":",gps_min,":",gps_sec
