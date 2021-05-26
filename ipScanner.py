import os
import time

import subprocess

devnull = open(os.devnull, 'wb')

pingList = []
activeList = []
activeCount = 0

print("IP Scan started")
for aralik in range(1,254):
    ip = "192.168.1." + "%d" % aralik
    pingList.append((ip, subprocess.Popen(['ping', '-c', '2', '-A', ip], stdout=devnull)))

ctr = 0
while pingList:    
    if(ctr%4 == 0):
        print("IP Scanning -" , end='\r')
    elif(ctr%4 == 1):
        print("IP Scanning \\" , end='\r')
    elif(ctr%4 == 2):
        print("IP Scanning |" , end='\r')
    else:
        print("IP Scanning /" , end='\r')
    ctr = ctr+1
    for i, (ip, proc) in enumerate(pingList[:]):
        if proc.poll() is not None:
            pingList.remove((ip, proc))
            if proc.returncode == 0:
                activeList.append(ip)
                activeCount = activeCount + 1
                print("\r                                ", end='\r')
                print("Active IP found: " + ip)
    time.sleep(.2)

devnull.close()

