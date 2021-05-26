import paho.mqtt.client as mqttClient
from tkinter import Tk, Label , Frame , Entry , Button, TOP, BOTTOM, LEFT, RIGHT, Toplevel
from ipScanner import activeList as devices

id = "0000"

def onConnect(client, userdata, flags, rc):
    client.subscribe("chatApp/#")

# The callback for when a PUBLISH message is received from the server.
def onMessage(client, userdata, msg):
    if "chatApp/id{}".format(id) in msg.topic:
        lastMessageText['text'] = msg.payload
    elif msg.topic == "chatApp/idList":
        client.publish("chatApp/idRsp", id)

def onEnter(event):
    client.publish("chatApp/subApp", event.widget.get())
    event.widget.delete(0, 'end')

client = mqttClient.Client()
client.on_connect = onConnect
client.on_message = onMessage
client.connect("localhost", 1883, 60)
client.loop_start()


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

print(devices)

root.mainloop()