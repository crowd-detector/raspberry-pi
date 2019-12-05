import asyncio
import websockets
import socket
import os
import requests
import urllib.request
import time

def internet_on():
    try:
        urllib.request.urlopen('http://www.google.com', timeout=5)
        return True
    except: 
        return False

async def hello():
    while True:
        if internet_on():
            print('Connected to internet')
            break
        else:
            print('Waiting for internet')
            time.sleep(5)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    IPAddr = s.getsockname()[0]

    #time.sleep(60)
    '''
    url = 'https://tmoswd3hb2.execute-api.us-east-1.amazonaws.com/dev/pi_start_setup'
    print(requests.post(url, json =
        {
        "cameraId": str(IPAddr),
        "ip": str(IPAddr),
        "streamLink": "https://www.youtube.com/watch?v=0Dzx3fEo8mk",
        "sshLink": "proxy21.rt3.io",
        "sshPort": "31478"
        }))
    '''

    exec_cmd = 'curl --header "Content-Type: application/json" --request POST --data \'{"cameraId": "' + str(IPAddr) + '", "ip": "' + str(IPAddr) + '", "streamLink": "https://www.youtube.com/watch?v=0Dzx3fEo8mk", "sshLink":"none", "sshPort":"none"}\' https://tmoswd3hb2.execute-api.us-east-1.amazonaws.com/dev/pi_start_setup'
    print(exec_cmd)
    os.system(exec_cmd)

    uri = "ws://ec2-3-88-188-83.compute-1.amazonaws.com:8765"

    async with websockets.connect(uri) as websocket:
        name = IPAddr
        await websocket.send(name)
        greeting = await websocket.recv()
        print(greeting)

        print("Wait for command")
        
        while True:
            try:
                command = await websocket.recv()
                print(command)
                command = command.decode()

                if command == "up":
                    os.system('curl -d "Up" http://'+str(IPAddr)+':8001/cmd')                 
                    await websocket.send("Moving cam up")
                    # do script to move cam up
                elif command == "down":
                    #print("down")
                    os.system('curl -d "Down" http://'+str(IPAddr)+':8001/cmd')
                    await websocket.send('Moving cam down')
                    # do script to move cam down
                elif command == "done":
                    
                    os.system('curl -d "Done" http://'+str(IPAddr)+':8001/cmd')                    
##                    os.system('python /home/pi/Pan-Tilt-HAT/RaspberryPi/web_Python/deploy.py')
                    await websocket.send('done')
                    # do script to end stream, etc.
                    break
                else:
                    await websocket.send('Got command "{command}"')

            except Exception as e:
                print(e)
                
                websocket = await websockets.connect(uri)
                await websocket.send(name + ' again')
                greeting = await websocket.recv()
                print(greeting)
        

asyncio.get_event_loop().run_until_complete(hello())
