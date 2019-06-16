#!/usr/bin/python

# Import Class MongoConntroller 
from sys import argv, exit, path
# from bson.json_util import dumps
import json, time, datetime, random
import requests
import time

#start_time = time.time()
if __name__ == "__main__":
    # if(len(argv) != 4):
    #     print ("Usage : python SendingData.py <token> <secret> <topic>")
    #     exit()

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
    print(toke)

    # End Block Code for Login

    # Start Block Code for Sending Data
    i = 0
    while i < 2:

        # Blok kode data Tanah
        #humidity=random.randint(65,79)
        #nitrogen=random.randint(29,42)
        #ph=random.randint(4,7)
        
        iot = {
                'ph':234,
                'protocol': ['0','3757','0','2988','219','2411','722','1795','1379','1101','2187','383','3109','0','4095','0','4095','0','4095','0'],
            }
        
        # Blok kode data polusi
        # temperatur=random.randint(32,34)
        # ozon=random.randint(65,73)
        # karbon=random.randint(42,49)
        # sulfur=random.randint(59,66)
        # partikulat=random.randint(31,33)
        
        # iot = {
        #         'temperatur':temperatur,
        #         'ozon':ozon,
        #         'karbon':karbon,
        #         'sulfur':sulfur,
        #         'partikulat':partikulat
        #     }
        print (iot)
        r = requests.post(
            "http://api.iotapps.belajardisini.com/topic/qwerty", 
            data = {
                'data': json.dumps(iot)
            },
            headers = {
                'Authorization': "Bearer {}".format(toke)
            })
        
        if(r.status_code==200):
            print (r.content)
        else:
            print(r.content)
            print("Sys: Error in sending Data")
            print("Sys: Trying to generate new token")
            r = requests.post(
            	url+"/login", 
                data=
                {
                    'token' : argv[1],
                    'secret': argv[2]
                })
            
            if(r.status_code != 200):
                print("Sys : Cannot Authorized Using Token and Secret Key")
                exit(0)
            
            token = json.loads(r.content)['token']
        
        time.sleep(5)
        i += 1
    # END Block Code for Sending Data
#runtime = time.time() - start_time
#print("runtime %s" % (runtime))
# print("throughput %s" % (100/runtime))