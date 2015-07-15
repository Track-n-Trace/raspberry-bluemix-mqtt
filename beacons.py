import time
import sys
import pprint
import functions
import os
from uuid import getnode as get_mac

send_url = 'http://freegeoip.net/json'

#Application API Keys from Internet of Things Service from IBM Bluemix
username = "a-rgecs9-arcrtd7ntm"
password = "0Y)xgiCXFAwKyzXh9j"

temp = username.split("-")
organization = temp[1]
#any string for type e.g. "JavaDevice"
deviceType = "Pi"

deviceId = str(hex(int(get_mac())))[2:]
deviceId = 'gateway_'+deviceId[:-1]

deviceCli = functions.initialize(username, password, organization, deviceType, deviceId)
deviceCli.connect()

#r = requests.get(send_url)
#j = json.loads(r.text)
#lat = j['latitude']
#lon = j['longitude']

#Manyata Tech Park IBM
lat = 13.048291
lon = 77.620382

#EGL IBM
#lat = 12.951432
#lon = 77.643296

print(lat, lon)
iter = 0

while(True):
	iter = iter + 1
	print(iter)
	os.system("hciconfig hci0 down")
	os.system("hciconfig hci0 up")
	os.system("sudo hcitool lescan --duplicates > result.txt &")
	os.system("sleep 5")
	os.system("sudo pkill --signal SIGINT hcitool")
	f = open('result.txt','r')
	count = 0
	assets = set()
	for line in f:
		if (count != 0 and count%2 == 0):
			#print line
			temp = line.split(" ")
			asset = temp[0]
			assets.add("asset_"+asset)
		count = count + 1
	f.close()

	assetsList = list(assets)


	#assetsString = ""
	#for asset in assetsList:
	#	asset = asset.replace(":","")
	#	asset = asset.lower()
	#	asset = 'asset_'+asset
	#	assetsString += asset+" , "

	#assetsString = assetsString[:-3]

	data = { 'name' : deviceId, 'assets' : assetsList, 'latitude': lat, 'longitude': lon}

	deviceCli.publishEvent("greeting","json",data)
	#time.sleep(1)
			
# Disconnect the device and application from the cloud
deviceCli.disconnect()
