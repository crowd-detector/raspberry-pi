#!/usr/bin/python
# -*- coding:utf-8 -*-
from bottle import get,post,run,route,request,template,static_file
from PCA9685 import PCA9685
import threading
import os
import socket
import time
import picamera     # Importing the library for camera module
from time import sleep
import requests

import subprocess
##import sys

import json
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
localhost = s.getsockname()[0]

##developerkey="MjYzQzBFRTMtNkVGRS00MkRFLUI3RTQtRjY1Q0RCMzQyMTFC"
##password="abc1234"
##username="henry.h.pham13@gmail.com"
##headers = {
##    "developerkey": str(developerkey)
##}
##body = {
##    "password": str(password),
##    "username": str(username)
##}
##
##url = "https://api.remot3.it/apv/v27/user/login"
##
##response = requests.post(url, data=json.dumps(body), headers=headers)
##response_body = response.json()
##
##print(response_body)
# resp_dict = json.loads(response_body)

##token = response_body['token']


##headers = {
##    "developerkey": str(developerkey),
##    # Created using the login API
##    "token": str(token)
##}

##url = "https://api.remot3.it/apv/v27/device/list/all"
##
##response = requests.get(url, headers=headers)
##response_body = response.json()
##
##
##deviceaddress = response_body['devices'][0]['deviceaddress']
##
##publicip = response_body['devices'][0]['devicelastip']

##headers = {
##    "developerkey": str(developerkey),
##    # Created using the login API
##    "token": str(token)
##}
##body = {
##    "deviceaddress": "80:00:00:00:01:03:01:96",
##    "wait":"true"
####    "hostip":str(publicip)
##}
##
##url = "https://api.remot3.it/apv/v27/device/connect"
##print("Here")
##
##response = requests.post(url, data=json.dumps(body), headers=headers)
##response_body = response.json()
##
##print(response_body)
##
##proxyserver = response_body['connection']['proxyserver']
##
##proxyport = response_body['connection']['proxyport']
##
##print(proxyserver,proxyport)
##
##
##s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
##s.connect(('8.8.8.8', 80))
##IPAddr = s.getsockname()[0]
##
##url = 'https://tmoswd3hb2.execute-api.us-east-1.amazonaws.com/dev/pi_start_setup'
##print(requests.post(url, json ={
##"cameraId": str(IPAddr),
##"ip": str(IPAddr),
##"streamLink": "https://www.youtube.com/watch?v=0Dzx3fEo8mk",
##"sshLink": str(proxyserver),
##"sshPort": str(proxyport)
##}))




pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

#Set the Horizontal vertical servo parameters
#period = 30
#HPulse = 0  #Sets the initial Pulse
#HStep = 0      #Sets the initial step length
#VPulse = 0  #Sets the initial Pulse
#VStep = 0      #Sets the initial step length


period = 60
HPulse = 1500  #Sets the initial Pulse
HStep = 0      #Sets the initial step length
VPulse = 1000  #Sets the initial Pulse
VStep = 0      #Sets the initial step length
DONE_SIGNAL=False


start = int(time.time())

pwm.setServoPulse(1,HPulse)
pwm.setServoPulse(0,VPulse)



@post("/cmd")
def cmd():
    global HStep,VStep, period,live_stream,DONE_SIGNAL
    code = request.body.read().decode()
    print "code ",code
##    period = 60 #secs
    if code == "Stop":
        HStep = 0
        VStep = 0
        print("stop")
    elif code == "Up":
        VStep = -5
        print("up")
        sleep(0.5)
        VStep = 0
    elif code == "Down":
        VStep = 5
        print("down")
        sleep(0.5)
        VStep = 0
    elif code == "Left":
        HStep = 5
        print("left")
        sleep(0.5)
        HStep = 0
    elif code == "Right":
        HStep = -5
        print("right")
        sleep(0.5)
        HStep = 0
    elif "Done" in code:
        print("Done")
        pwm.exit_PCA9685()
        os.system('killall raspivid && killall avconv')
        periodfunc()

        #live_stream.term()
##        DONE_SIGNAL=True
##        camera.stop_recording()
##        camera.close() 
##        stream.stdin.close() 
##        stream.wait() 
##        print("Camera safely shut down") 
##        print("Good bye")
    return "OK"

def periodfunc():
    
    print('Taking picture')
##    for i in range(20):
    os.system('raspistill -o /home/pi/Desktop/image.jpg')
    
##    scp -i /home/pi/Desktop/crowdkey.pem /home/pi/Desktop/image.jpg ec2-user@ec2-35-174-116-80.compute-1.amazonaws.com:/home/ec2-user/crowddetector/backend/images
    os.system('scp -v -i /home/pi/Desktop/crowdkey.pem /home/pi/Desktop/image.jpg ec2-user@ec2-3-88-188-83.compute-1.amazonaws.com:/home/ec2-user/crowddetector/backend/images')   
##    while True:
##        if os.system('rsync -rave "/home/pi/Desktop/crowdkey.pem" /home/pi/Desktop/image.jpg ec2-user@ec2-35-174-116-80.compute-1.amazonaws.com:/home/ec2-user/crowddetector/backend/images'):              
##    os.system('./home/pi/Pan-Tilt-HAT/RaspberryPi/web_Python/push.sh')
    os.system('curl --header "Content-Type: application/json" --request POST --data \'{"cameraId": "' + str(localhost) + '","fileName": "image.jpg"}\' https://tmoswd3hb2.execute-api.us-east-1.amazonaws.com/dev/detection')
##            break
    threading.Timer(period, periodfunc).start()
    


def stream():
##    elif "Begin" in code:
    YOUTUBE="rtmp://a.rtmp.youtube.com/live2/" 
    KEY= "ceys-ugrq-tu6m-5dj1"#ENTER PRIVATE KEY HERE#
    os.system('raspivid -o - -t 0 -fps 30 -b 6000000 | avconv -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/ceys-ugrq-tu6m-5dj1')
##
##        stream_cmd = ' avconv -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - -vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv ' + YOUTUBE + KEY 
##        stream_pipe = subprocess.Popen(stream_cmd, shell=True, stdin=subprocess.PIPE) 
##        camera = picamera.PiCamera(resolution=(640, 480), framerate=25) 
##
##        ##def stream_dev():
##        
##        now = time.strftime("%Y-%m-%d-%H:%M:%S") 
##        camera.framerate = 25 
##        camera.vflip = True 
##        camera.hflip = True 
##        camera.start_recording(stream_pipe.stdin, format='h264', bitrate = 2000000) 
##        while True:
##            camera.wait_recording(1)
        
##def stop_stream():
##    for line in os.popen("ps ax | grep raspivid | grep -v grep"):
##        fields = line.

        
def timerfunc():
    global HPulse,VPulse,HStep,VStep,pwm,start,live_stream
    end=int(time.time())
##    if(DONE_SIGNAL):
##        live_stream.kill()
##        sys.exit()
    if(HStep != 0):
        HPulse += HStep
        if(HPulse >= 2500): 
            HPulse = 2500
        if(HPulse <= 500):
            HPulse = 500
        #set channel 2, the Horizontal servo
        pwm.start_PCA9685()
        pwm.setServoPulse(1,HPulse)
        start = int(time.time())  

    if(VStep != 0):
        VPulse += VStep
        if(VPulse >= 2500): 
            VPulse = 2500
        if(VPulse <= 500):
            VPulse = 500
        #set channel 3, the vertical servo
        pwm.start_PCA9685()
        pwm.setServoPulse(0,VPulse)   
        start = int(time.time())
        
    end = int(time.time())
    if((end - start) > 2):
        pwm.exit_PCA9685()        
        start = int(time.time())

    
    global t        #Notice: use global variable!
    t = threading.Timer(0.02, timerfunc)
    t.start()
    
try:
##    t2 = threading.Thread()
##    t2.setDaemon(True)
##    t2.start()
       
    t = threading.Timer(0.02, timerfunc)
    t.setDaemon(True)
    t.start()
    
    periodfunc()
    processThread = threading.Thread(target=stream)
    processThread.start()
    #stream()
    
    

    run(host=localhost, port="8001")

except:
    pwm.exit_PCA9685()
    print("\nProgram end")
    exit()
