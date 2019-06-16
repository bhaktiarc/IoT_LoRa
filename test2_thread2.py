#import LoRaReceiver
import config_lora
import sx127x
import socket
import paho.mqtt.client as mqtt_client
import threading
import json
import RPi.GPIO as GPIO


#inisiasi client mqtt
test = mqtt_client.Client()

#Koneksikan ke broker
test.connect("127.0.0.1", 1883)

def fwdToMQTT(lora):
    try:
        payload = lora.read_payload()
        #print("*** Received message ***\n{}".format(payload.decode()))
        payload = json.loads(payload.decode())
        #dibagi 2 -> payload topic dan payload data

        print (payload["topic"], payload["data"])
        #publish ke broker
        test.publish(payload["topic"], payload["data"])
        
    except Exception as e:
        print(e)
        
def main():

    try:
        GPIO.setwarnings(False)
        controller = config_lora.Controller()

        lora = controller.add_transceiver(sx127x.SX127x(name = 'LoRa'),
                                          pin_id_ss = config_lora.Controller.PIN_ID_FOR_LORA_SS,
                                          pin_id_RxDone = config_lora.Controller.PIN_ID_FOR_LORA_DIO0)
        print('lora', lora)

        #threads = list()

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
    except Exception as e :
        print ("terjadi kesalahan")
        print (e)
    #finally:
        #GPIO.cleanup()
        

if __name__ == '__main__':
    main()