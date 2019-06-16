import config_lora
import sx127x
import socket
import paho.mqtt.client as mqtt_client
import threading
import json
import RPi.GPIO as GPIO
# Import Class MongoConntroller 
from sys import argv, exit, path
# from bson.json_util import dumps
import json, time, datetime, random
import requests
import time


# Block Code for Login
r = requests.post(
    "http://api.iotapps.belajardisini.com/user/login", 
    data=
    {
    'token' : 'f25eb49fec7c1231ff7b435a3b5be23274b793df',
    'secret': 'b7b900636c24c67f03c758ccc92ca44b'
    })
if(r.status_code != 200):
    print("Sys : Cannot Authorized Using Token and Secret Key")
    exit(0)
toke = json.loads(r.content.decode())['token']
print("terhubung dengan iotapps")

# End Block Code for Login

def fwdToMQTT(lora):
    try:
        payload = lora.read_payload()
        #print("*** Received message ***\n{}".format(payload.decode()))
        #ngeload json dari sensor esp32
        payload = json.loads(payload.decode())

        split = payload["topic"].split("/")
        topic = split[0]
        idSensor = split[1]
        dataecg = payload["data"]
        
        #dibagi 2 -> payload topic dan payload data
        print (payload["topic"])
        #print (payload["data"])
        #print (payload)
        #bikin json dari array payload data 
        #payload2 = json.dumps(payload["data"])
        #publish ke broker
        #test.publish(payload["topic"], payload2)
        #print (toke)
        
        ecg = {
            'idSensor': idSensor,
            'dataEcg': dataecg,
        }
        r = requests.post(
            "http://api.iotapps.belajardisini.com/topic/ecg",
            data = {
                'data' : json.dumps(ecg)
            },
            headers = {
                'Authorization': "Bearer {}".format(toke)
            })
        #print (idSensor)
        print (ecg)
        print (r.content)
        print("berhasil kirim data ke iotapps")
    except Exception as e:
        print(e)

def main():

    try:
        #GPIO.setwarnings(False)
        controller = config_lora.Controller()

        lora = controller.add_transceiver(sx127x.SX127x(name = 'LoRa'),
                                          pin_id_ss = config_lora.Controller.PIN_ID_FOR_LORA_SS,
                                          pin_id_RxDone = config_lora.Controller.PIN_ID_FOR_LORA_DIO0)
        print('lora', lora)

        #LoRaReceiver.receive(lora)
        print("LoRa Receiver")
        while True:         
            if lora.receivedPacket():
                t = threading.Thread(target=fwdToMQTT(lora))
                #threads.append(t)
                t.start()
                #print (threads)
                    
    except KeyboardInterrupt:
        print ("Program dihentikan dengan interupsi")
        GPIO.cleanup()
    except Exception as e :
        print ("terjadi kesalahan")
        print (e)
    #finally:
        #GPIO.cleanup()

if __name__ == '__main__':
    main()