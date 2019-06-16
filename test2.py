#import LoRaReceiver
import config_lora
import sx127x
import socket
import paho.mqtt.client as mqtt_client
import threading
import json
import RPi.GPIO as GPIO


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
                
                try:
                    payload = lora.read_payload()
                    #print("*** Received message ***\n{}".format(payload.decode()))
                except Exception as e:
                    print(e)

                #inisiasi client mqtt
                test = mqtt_client.Client()

                #Koneksikan ke broker
                test.connect("127.0.0.1", 1883)

                payload = json.loads(payload.decode())
                #dibagi 2 -> payload topic dan payload data

                print (payload["topic"], payload["data"])
                #publish ke broker
                test.publish(payload["topic"], payload["data"])
    except KeyboardInterrupt:
        print ("Program Stop Running by interruption!")
    except Exception as e :
        print ("Error Occured:")
        print (e)
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()



