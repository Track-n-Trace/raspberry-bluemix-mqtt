import sys
import usb
import functions
import os
from uuid import getnode as get_mac

SCAN_CODES = ["","err","err","err","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","1","2","3","4","5","6","7","8","9","0","\n","Esc","BSp","\t"," "]

#VENDOR_ID = 0x4b3
#PRODUCT_ID = 0x3025

VENDOR_ID = 0X8ff
PRODUCT_ID = 0x9

#Application API Keys from Internet of Things Service from IBM Bluemix
username = "<API-KEY>"
password = "<AUTHENTICATION-TOKEN>"

temp = username.split("-")
organization = temp[1]
#any string for type e.g. "JavaDevice"
deviceType = "Pi"

deviceId = str(hex(int(get_mac())))[2:]
deviceId = 'gateway_'+deviceId[:-1]

deviceCli = functions.initialize(username, password, organization, deviceType, deviceId)
deviceCli.connect()

#Manyata Tech Park IBM
#lat = 13.048291
#lon = 77.620382

#EGL IBM
lat = 12.951432
lon = 77.643296

print lat, lon
iter = 0


device = usb.core.find(idVendor = VENDOR_ID, idProduct = PRODUCT_ID)

if device.is_kernel_driver_active(0):
	device.detach_kernel_driver(0)

device.set_configuration()
endpoint = device[0][(0,0)][0]
#print device.is_kernel_driver_active(0)

counter = 0
rfid = ""
ENTER = False
assets = []
while(True):
	try:
		data = device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
		data = filter(lambda a: a != 0, data)
		if (len(data) <> 0):
			for x in data:
				if (x == 40):
					ENTER = True
				else:
					rfid = rfid + SCAN_CODES[x]
	except:
		data = "None"

	if (data <> "None"):
		if (ENTER):
			ENTER = False
			#print rfid
			rfid = 'asset_'+rfid
			if (rfid in assets):
				assets.remove(rfid)
			else:
				assets.append(rfid)
			data = { 'name' : deviceId, 'assets' : assets, 'latitude': lat, 'longitude': lon}
			deviceCli.publishEvent("greeting","json",data)
			
			print assets
			rfid = ""

deviceCli.disconnect()
