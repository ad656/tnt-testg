#Much simpler and better version of gw_monitor
#Changes made by A D
#for TagNTrac

import paho.mqtt.client
import time
import struct
import queue
import sys
import ssl
import json
import datetime

#This IMEI is reserved for simulation only
IMEI                = 351521101031151
IMEI                = 868617060015775

AWS_ENDPOINTURL_JR  = "a3jycw9whepmvi-ats.iot.us-east-1.amazonaws.com"
AWS_ENDPOINTURL_TNT = "a2fyxktdys7yyx-ats.iot.us-east-1.amazonaws.com"
MAX_AWS_STRLEN =64
AWS_PORT = 8883
sub_delay =0.05
loggers = []

#GW = 'deviceId-354616090682316' #-venu
#GW = 'deviceId-354616090650990' #-airsave
#GW = 'deviceId-354616090650883' #-airsave
#GW = 'deviceId-354616090683082' #-airsave
#GW = 'deviceId-354616090639969' #-airsave

#GW = 'deviceId-354616091134838' #-wen v82
#GW = 'deviceId-354616091125455'  # v82
GW = 'deviceId-354616091004130' #83
#GW = "deviceId-354616091134754"
#GW = "deviceId-354616091141239"
#GW = "deviceId-354616091113477"
#GW = "deviceId-354616091000575"

GW = 'deviceId-354616091124235'
#GW = 'deviceId-354616091140538'
#GW = 'IG60-44E888'
##GW = 'IG60-64529C'
##GW = 'IG60-1'
##GW = 'IG60-64F250'
#GW = 'IG60-3'
#GW = 'OWEN-PI3'
#GW = 'GWS79025'
##GW = 'GWT34552'
#GW = 'GWT34550'
##GW = 'GWT32230'
#GW = 'GWT32226'
##GW = 'GWT32230'
##GW = 'GWT34555'
##GW = 'GWT34553'
#GW = 'GWT33467'
#GW = "deviceId-354616091113477"
#GW = 'GWS97118'
#GW = 'GWS97127'
#GW = 'GWS97118'
#GW = 'GWS97122'
#GW = 'GWT50605'
#GW = 'GWT50613'#good
#GW = 'GWT50620'
#GW = 'GWT50641' #gggood
##GW = 'GWT50594'
##GW = 'GWT50627'

##GW = 'GWT34554'
##GW = 'GWS97059'
##GW = 'GWS97069'
##GW = 'GWS97119'
#GW = 'GWT53488'
#GW = 'GWS97112'
#GW = 'GWS96929'
#GW = 'GWS96915'
#GW =  'GWT53479'
GW = 'GWS97099'
#GW = 'GWS96925'
#GW = 'T50598GWT53478'
#GW = 'GWS96918'
#GW = 'GWS97130'
#GW = 'GWS96911'
#GW = 'GWS96916'
#GW =  'GWT53488'

msg_queue = queue.Queue()
sub_list =[
    [f'$aws/things/{GW}/shadow/get',0],
    [f'$aws/things/{GW}/shadow/get/accepted',0],
    [f'$aws/things/{GW}/shadow/update',0],
    [f'$aws/things/{GW}/shadow/update/accepted',0],
    [f'$aws/things/{GW}/shadow/update/rejected',0],
    [f'$aws/things/{GW}/shadow/update/documents',0],
    
    [f'$aws/things/{GW}/shadow/update/delta',0],
    [f'blegw/{GW}/ftl1',0],
    [f'blegw/{GW}/rsp',0],
    [f'blegw/{GW}/adv',0], #too many info....
##    [f'blegw/{GW}/other_adv',0], #too many info....
#    [f'blegw/{GW}/dbg',0],
#    ['logger/C46A7CF91760/data',0],

#    ['blegw/deviceId-354616091134838/ftl1',0],
#    ['blegw/deviceId-354616091134838/rsp',0],
#    ['blegw/deviceId-354616091134838/adv',0],
#    ['dtc/351521101011948/v1',0],
#    ['dtc/351521101016020/v1',0],
#    ['dtc/351521101016020/v1',0],
#    ['dtc/351521101730687/v1',0],
#    ['dtc/351521101723955/v1',0],
    
#    ['dtc/351521101023307/v1',0],
#    ['dtc/351521101032951/v1',0],
#    ['dtc/351521101032084/v1',0],
#    ['dtc/351521101015345/v1',0],
#    ['dtc/351521101015402/v1',0],
#    ['dtc/351521101022374/v1',0],
#    ['dtc/351521101022473/v1',0],

#   ['dtc/351521101031151/v1',0],
#   ['dtc/351521101022986/v1',0],
##    ['dtc/351521101016020/v1',0],
##    ['dtc/351521101016020/v1/accepted',0],
##    ['dtc/351521101024081/v1',0],
##    ['dtc/351521101024081/v1/accepted',0],
##    ['dtc/351521101730687/v1',0],
##    ['dtc/351521101730687/v1/accepted',0],
##    ['dtc/351521101723955/v1',0],
##    ['dtc/351521101723955/v1/accepted',0],
##    ['dtc/868617060005222/v1',0],
##    ['dtc/868617060005222/v1/accepted',0],
##    ['dtc/868617060015775/v1',0],
##    ['dtc/868617060015775/v1/accepted',0],
##    ['dtc/868617060015551/v1',0],
##    ['dtc/868617060015551/v1/accepted',0],
##    ['dtc/868617060015775/v1',0],
##    ['dtc/868617060015775/v1/accepted',0],
##
    ]

caPath = "AWS_cert/AmazonRootCA1.pem"
certPath = "AWS_cert/certificate.pem.crt"
keyPath = "AWS_cert/private.pem.key"

#file_name=f'AWS{int(time.time())}.txt'
#file = open(file_name,mode='a')


def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print(int(time.time()), "AWS MQTT Broker connected")
        client.connected_flag = True
        # if reconnected need to do sub again
        time.sleep(0.01)
        subscribe(client,'AWS MQTT Broker',sub_list)
    else:
        print(rc,"AWS MQTT Broker connection failed!")
    
def on_message(client,userdata,msg):
    msg_queue.put(msg)

    while not msg_queue.empty():
        message = msg_queue.get()
        print(int(message.timestamp), message.topic)
        payload = message.payload.decode()  # Convert payload bytes to string
        #print(payload)
        if payload[88] is ".":
            print(f"timestamp: {datetime.datetime.now()},Logger ID:{payload[31:44]}, Temperature: {payload[86:90]}")
            if payload[31:44] not in loggers:
                loggers.append(payload[31:44])
                print(f"{loggers}, Unique loggers found:{len(loggers)}")
        elif payload[87] is ".":
            print(f"timestamp: {payload[13:24]}, Logger ID:{payload[31:44]}, Temperature: {payload[86:89]}")
            if payload[31:44] not in loggers:
                loggers.append(payload[31:44])
                print(f"{loggers}, Unique logger found:{len(loggers)}")

    
#    while not msg_queue.empty():
 #       message = msg_queue.get()
  #      print(int(message.timestamp), message.topic)
   #     print(message.payload)
    #    #file.write(f'{int(message.timestamp)} {message.topic}')
     #   client.log_handle.write((message.payload).decode())
      #  client.log_handle.write('\n')
       # client.log_handle.flush()

def subscribe(client, name, sub_list):
    print(f'{int(time.time())} {name} starts subscription')
    for [topic, qos] in sub_list:
        try:
            client.subscribe(topic,qos)
            time.sleep(sub_delay)
            print(int(time.time()), name, topic, "qos=",qos, " subscribed")
        except:
            print(int(time.time()), name, topic, "qos=",qos, " failed sub")

def monitor(client):
    
    #file = open(file_name,mode='a')
    file_name = f'AWS_log_{int(time.time())}.txt'
    client.log_handle = open(file_name,mode='a')
    #subscribe(client,'AWS MQTT Broker',sub_list)
    

def simulator(client):
    pass

if __name__=="__main__":
       
    aws=paho.mqtt.client.Client()
    aws.on_connect = on_connect
    aws.on_message = on_message
    
    aws.tls_set(caPath,
                    certfile=certPath,
                    keyfile=keyPath,
                    cert_reqs=ssl.CERT_REQUIRED,
                    tls_version=ssl.PROTOCOL_TLSv1_2,
                    ciphers=None)

    #monkey patch to add one flag for aws
    aws.connected_flag = False
    
    if aws.connect(AWS_ENDPOINTURL_TNT,AWS_PORT,60) == 0:
        print(int(time.time()), "AWS MQTT Broker connecting")

    aws.loop_start()
    time.sleep(0.5)
    
    while not aws.connected_flag:
        print(int(time.time()), "AWS MQTT Broker waiting")
        time.sleep(0.01)

    
    time.sleep(0.01)
    monitor(aws)
    #subscribe(aws,'AWS MQTT Broker',sub_list)
    #client.log_handle.close()
    #client.loop_stop()
