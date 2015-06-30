import time
import sys
import pprint
import urllib, urllib2, base64, json
from uuid import getnode as get_mac

import ibmiotf.application
import ibmiotf.device

import os
import requests
import json

send_url = 'http://freegeoip.net/json'

#Application API Keys from Internet of Things Service from IBM Bluemix
username = <API-USERNAME>
password = <API-KEY>

#organization and deviceType of Internet of Things Service
organization = <ORGANIZATION NAME>
#any string for type e.g. "JavaDevice"
deviceType = <ANY DEVICE TYPE>

deviceId = str(hex(int(get_mac())))[2:]
deviceId = 'gateway_'+deviceId[:-1]

request = urllib2.Request("https://"+organization+".internetofthings.ibmcloud.com/api/v0001/devices/"+deviceType)
base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
request.add_header("Authorization", "Basic %s" % base64string)
result = urllib2.urlopen(request)
data =  result.read()

found = False
data = json.loads(data)
for item in data:
	if (item['id'] == deviceId):
		found = True

if (not found):
	values = {'type':deviceType,'id':deviceId}

	request = urllib2.Request("https://"+organization+".internetofthings.ibmcloud.com/api/v0001/devices")
	request.add_header("Authorization", "Basic %s" % base64string)
	request.add_header('Content-Type', 'application/json')
	result = urllib2.urlopen(request, json.dumps(values))
	data =  result.read()
	data = json.loads(data)
	f = open("authToken","w")
	f.write(data["password"])
	f.close()
	print "Registered!"

f = open("authToken","r")
appId = "gateway_"+deviceId
authMethod = "token"
authToken = f.read()
f.close()

print deviceId
# Initialize the device client.
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
	print(str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

#r = requests.get(send_url)
#j = json.loads(r.text)
#lat = j['latitude']
#lon = j['longitude']

#Manyata Tech Park IBM
#lat = 13.048291
#lon = 77.620382

#EGL IBM
lat = 12.951432
lon = 77.643296

print lat, lon
iter = 0

while(True):
	iter = iter + 1
	print iter
	os.system("hciconfig hci0 down")
	os.system("hciconfig hci0 up")
	os.system("sudo hcitool lescan --duplicates > result.txt &")
	os.system("sleep 5")
	os.system("sudo pkill --signal SIGINT hcitool")
	f = open('result.txt','r')
	count = 0
	assets = set()
	for line in f:
		if (count <> 0 and count%2 == 0):
			#print line
			temp = line.split(" ")
			asset = temp[0]
			assets.add(asset)
		count = count + 1
	f.close()

	assetsList = list(assets)


	assetsString = ""
	for asset in assetsList:
		asset = asset.replace(":","")
		asset = asset.lower()
		asset = 'asset_'+asset
		assetsString += asset+" , "

	assetsString = assetsString[:-3]

	data = { 'name' : deviceId, 'assets' : assetsString, 'latitude': lat, 'longitude': lon}

	deviceCli.publishEvent("greeting","json",data)
	#time.sleep(1)
			
	# Disconnect the device and application from the cloud

deviceCli.disconnect()
