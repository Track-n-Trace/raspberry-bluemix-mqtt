import requests
import json
import ibmiotf.application
import ibmiotf.device
import urllib, urllib2, base64, json

def initialize(username, password, organization, deviceType, deviceId):
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
		return deviceCli
	except Exception as e:
		print(str(e))
		sys.exit()
