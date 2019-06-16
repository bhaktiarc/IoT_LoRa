import socket
import paho.mqtt.client as mqtt_client
import threading
import json

#inisiasi client mqtt
subscriber = mqtt_client.Client()

#Koneksikan ke broker
subscriber.connect("192.168.1.22", 1883)


def handle_message(client, userdata, msg):
	
	payload = json.loads(msg.payload.decode())

	#print topik dan payload
	print("Topik : " + msg.topic + "\nPayload : " + payload)

	#print (data)
	for x in payload:
		txtFile = open("ecg.txt", "a")
		txtFile.write(x)
		txtFile.write("\n")
		txtFile.close()

try:
	while True :
	    # Daftarkan fungsinya untuk event on_message
	    subscriber.on_message = handle_message
	    # Subscribe ke sebuah topik
	    subscriber.subscribe("ecg/#")
	    # Loop forever
	    subscriber.loop_forever()
except Exception as e:
	print (e)
except KeyboardInterrupt:
	print ("Program Stop Running by interruption!")
else:
	pass
finally:
	pass
	