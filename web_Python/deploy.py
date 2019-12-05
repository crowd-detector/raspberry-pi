import threading
import os
import socket
import time

from bottle import get,post,run,route,request,template,static_file
import requests

localhost='8.8.8.8'
period=120
count=0
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
localhost = s.getsockname()[0]

url = 'https://tmoswd3hb2.execute-api.us-east-1.amazonaws.com/dev/detection'
print(requests.post(url, json = {"cameraId": str(localhost),"fileName": "imag.jpg"}))

@post("/cmd")
def cmd():
    global period
    code = request.body.read().decode()
    print "code ",code
    #period = 30 #secs
  
    if "Ped" in code:
        where = code.find("Ped")
        period = int(code[where+3:])        

    return "OK"




def periodfunc():

    global period,count
    print('Taking picture')
##    for i in range(20):
    os.system('raspistill -o /home/pi/Desktop/1119/'+time.strftime("%Y%m%d-%H%M%S")+'.jpg')
    os.system('scp -i /home/pi/Desktop/crowdkey.pem /home/pi/Desktop/imag.jpg ec2-user@ec2-35-174-116-80.compute-1.amazonaws.com/crowddetector/backend/images') 
##   	count+=1
    
    
    
    threading.Timer(period, periodfunc).start()
    

periodfunc()


run(host=localhost, port="8001")

