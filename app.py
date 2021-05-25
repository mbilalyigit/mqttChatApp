import paho.mqtt.client as mqttClient
from tkinter import Tk, Label

id = "0987"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if("chatApp/id{}".format(id) in msg.topic):
        lastMessageText['text'] = msg.payload

client = mqttClient.Client()
client.on_connect = on_connect
client.on_message = on_message

# window = Tl.Tk()

client.connect("localhost", 1883, 60)
client.subscribe("chatApp/#")
client.loop_start()
print("Hello World!")

root = Tk()
lastMessageHeader = Label(root, text="Last Message:")
lastMessageHeader.pack()
lastMessageText = Label(root, text="")
lastMessageText.pack()
root.mainloop()