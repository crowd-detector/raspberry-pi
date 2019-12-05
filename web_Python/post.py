import requests
##import subprocess
##import sys

import json

developerkey="MjYzQzBFRTMtNkVGRS00MkRFLUI3RTQtRjY1Q0RCMzQyMTFC"
password="abc1234"
username="henry.h.pham13@gmail.com"
headers = {
    "developerkey": str(developerkey)
}
body = {
    "password": str(password),
    "username": str(username)
}

url = "https://api.remot3.it/apv/v27/user/login"

response = requests.post(url, data=json.dumps(body), headers=headers)
response_body = response.json()

#print(response_body)
# resp_dict = json.loads(response_body)

token = response_body['token']


##headers = {
##    "developerkey": str(developerkey),
##    # Created using the login API
##    "token": str(token)
##}
##
##url = "https://api.remot3.it/apv/v27/device/list/all"
##
##response = requests.get(url, headers=headers)
##response_body = response.json()
##
##
##deviceaddress = response_body['devices'][0]['deviceaddress']
##
##publicip = response_body['devices'][0]['devicelastip']

headers = {
    "developerkey": str(developerkey),
    # Created using the login API
    "token": str(token)
}
body = {
    "deviceaddress": "80:00:00:00:01:03:01:96",
    "wait":"true"
}

url = "https://api.remot3.it/apv/v27/device/connect"
print("Here")

response = requests.post(url, data=json.dumps(body), headers=headers)
response_body = response.json()


print(json.dumps(response_body, indent=4))

proxyserver = response_body['connection']['proxyserver']

proxyport = response_body['connection']['proxyport']

print(proxyserver,proxyport)


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
IPAddr = s.getsockname()[0]

url = 'https://tmoswd3hb2.execute-api.us-east-1.amazonaws.com/dev/pi_start_setup'
print(requests.post(url, json ={
"cameraId": str(IPAddr),
"ip": str(IPAddr),
"streamLink": "https://www.youtube.com/watch?v=0Dzx3fEo8mk",
"sshLink": str(proxyserver),
"sshPort": str(proxyport)
}))
