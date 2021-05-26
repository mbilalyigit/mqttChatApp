import paho.mqtt.client as mqttClient
from tkinter import Tk, Label , Frame , Entry , Button, TOP, BOTTOM, LEFT, RIGHT, Toplevel
import time
import random
from datetime import datetime
random.seed(datetime.now().second + datetime.now().microsecond)
id_int = random.randint(0, 9999)
print("RNG ID is: " + "{}".format(id_int))
id = "{}".format(id_int)

from ipScanner import activeList as devices

def onConnect(client, userdata, flags, rc):
    print("rc: " + "{}".format(rc))
    client.subscribe("chatApp/#")

# The callback for when a PUBLISH message is received from the server.
def onMessage(client, userdata, msg):
    if "chatApp/id{}".format(id) in msg.topic:
        lastMessageText['text'] = msg.payload
    elif "chatApp/subApp" in msg.topic:
        lastMessageText['text'] = msg.payload
    elif msg.topic == "chatApp/idList":
        client.publish("chatApp/idRsp", id)
    

def onEnter(event):
    msg =   event.widget.get()
    print(msg)
    client.publish("chatApp/subApp", msg)
    event.widget.delete(0, 'end')

client = mqttClient.Client()
client.on_connect = onConnect
client.on_message = onMessage

chatDeviceList = []

if(devices.count == 0):
    quit()
else:
    for device in devices:
        try:
            client.connect(device , 1883, 60)
            chatDeviceList.append(device)
            client.disconnect()
        except:
            print("Couldn't connect to mqtt broker at -> " + device)

print("Waiting for Cooldown...")
time.sleep(1)

#TODO select device from list; for now, go with first one
if(chatDeviceList):
    mqttDeviceAddress = chatDeviceList[0]
    print("Connecting to IP: " + mqttDeviceAddress)
    client.connect(device , 1883, 60)
    client.loop_start()
else:
    print("No Local device to connect")
    print("Connectiong to Local MQTT broker")
    try:
        client.connect("localhost", 1883, 60)
    except:
        print("Local MQTT broker is down.\r\n quitting...")
        quit()

root = Tk()

settingsButton = Button(root, text="Settings")
settingsButton.pack(side=TOP)

topFrame = Frame(root)
topFrame.pack(side=TOP)
lastMessageHeader = Label(topFrame, text="Last Message:")
lastMessageHeader.pack(side=LEFT)
lastMessageText = Label(topFrame, text="")
lastMessageText.pack(side=RIGHT)

buttomFrame = Frame(root)
buttomFrame.pack(side=BOTTOM)
messageLabel = Label(buttomFrame, text="Your message:")
messageLabel.pack(side=LEFT)
messageText = Entry(buttomFrame)
messageText.pack(side=LEFT)
messageText.bind('<Return>', onEnter)

root.mainloop()