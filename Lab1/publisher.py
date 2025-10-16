import paho.mqtt.client as mqtt
import numpy as np
import time


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        print("Connection returned result: Success")

def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print("Disconnected with result code: " + str(reason_code))

def on_message(client, userdata, message):
    print('Received message: "' + str(message.payload) + '" on topic "' +
          message.topic + '" with QoS ' + str(message.qos))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

client.connect_async('test.mosquitto.org')

client.loop_start()

for i in range(10):
    # Extract the single float from the numpy array before publishing
    random_float = float(np.random.random(1)[0])
    client.publish('ece180d/test', random_float, qos=1)
    print(f"HI GUYS :) have a great day!!!")

# Give the client time to send the messages
time.sleep(2)


client.loop_stop()
client.disconnect()
