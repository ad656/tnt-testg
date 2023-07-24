import paho.mqtt.client
import time
import struct
import queue
import sys
import ssl
import json

##import email
##import pwd
import requests
import json
import time
import random
import datetime
import sys
import pandas as pd
import pprint


sdlist1 = 'sdlist1.txt'
sdlist2 = 'sdlist2.txt'
sdlist3 = 'sdlist3.txt'
sdlist4 = 'sdlist4.txt'
sdlist5 = 'sdlist5.txt'
sdlist6 = 'sdlist6.txt'
sdlist7 = 'sdlist7.txt'
sdlist8 = 'sdlist8.txt'
sdlist9 = 'sdlist9.txt'
sdlist10 = 'sdlist10.txt'
sdlist11 = 'sdlist11.txt'
sdlist19 = 'sdlist19.txt'
sdlist20 = 'sdlist20.txt'
sdlist  = 'sdlist.txt'
sdlist_allversions ='sdlist_allversions.txt'
fname_devlist = [sdlist6,
                 sdlist7,
                 sdlist8,
                 sdlist9,
                 sdlist10,
                 sdlist1,
                 sdlist2,
                 sdlist3,
                 sdlist4,
                 sdlist5,]
name_devlist='sdlist1000'
#fname_devlist = [sdlist_allversions]
#name_devlist = 'sdlist_allversions'
#fname_devlist = [sdlist11]
#name_devlist = 'sdlist11'
#fname_devlist = [sdlist20]
#name_devlist = 'sdlist7'
fname_devlist = [sdlist]
list_size = 11
#list_size = 2

payload={}
GW = 'IG60-64F250'
GW = 'deviceId-354616091140538'
GW = 'deviceId-354616091124235' # new SP v79
#GW = 'IG60-1'
GW = 'deviceId-354616091140538'
GW = 'deviceId-354616091124235' # new SP v79
#GW = 'deviceId-354616091004130' #v83
maxDelay = 160
maxDelay = 100
cycle = 3
this = []

#GW = 'deviceId-354616091124235' # new SP v79

GW = 'GWT53475'
GW = 'GWT53475'
GW = 'GWT53485'
GW = 'GWT53477'

cmd = 'gethealth'
cmd = 'reset'
cmd = 'configAndReset'
cmd = 'read'
#cmd = 'reset'
#cmd = 'alert'
#cmd = random.choice(['read','configAndReset'])
    
apiToken = None
apiKey = None

id_inv = "inventory@tagntrac.io"
pwd_inv = "T6wkccwd#1"

id = id_inv
pwd = pwd_inv

AWS_ENDPOINTURL_JR  = "a3jycw9whepmvi-ats.iot.us-east-1.amazonaws.com"
AWS_ENDPOINTURL_TNT = "a2fyxktdys7yyx-ats.iot.us-east-1.amazonaws.com"
MAX_AWS_STRLEN =64
AWS_PORT = 8883
sub_delay =0.05
msg_queue = queue.Queue()
sub_list =[
##    [f'$aws/things/{GW}/shadow/get',0],
##    [f'$aws/things/{GW}/shadow/get/accepted',0],
##    [f'$aws/things/{GW}/shadow/update',0],
##    [f'$aws/things/{GW}/shadow/update/accepted',0],
##    [f'$aws/things/{GW}/shadow/update/rejected',0],
##    [f'$aws/things/{GW}/shadow/update/documents',0],

    [f'$aws/things/{GW}/shadow/update/delta',0],
    [f'blegw/{GW}/ftl1',0],
    [f'blegw/{GW}/rsp',0],
##    [f'blegw/{GW}/adv',0], #too many info....
##    [f'blegw/{GW}/dbg',0], #too many info...
    ]
caPath = "c:/Users/tagnt/Downloads/tnt-testg/ca/AmazonRootCA1.pem"
certPath = "c:/Users/tagnt/Downloads/tnt-testg/ca/certificate.pem.crt"
keyPath = "c:/Users/tagnt/Downloads/tnt-testg/ca/private.pem.key"

def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print(int(time.time()), "AWS MQTT Broker cfonnected")
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
        print(message.payload)
        #file.write(f'{int(message.timestamp)} {message.topic}')
##        client.log_handle.write((message.payload).decode())
##        client.log_handle.write('\n')
##        client.log_handle.flush()

def subscribe(client, name, sub_list):
    print(f'{int(time.time())} {name} starts subscription')
    for [topic, qos] in sub_list:
        try:
            client.subscribe(topic,qos)
            time.sleep(sub_delay)
            print(int(time.time()), name, topic, "qos=",qos, " subscribed")
        except:
            print(int(time.time()), name, topic, "qos=",qos, " failed sub")




class apiUser:
    def __init__(self, id, pwd):
        self.id = id
        self.pwd = pwd

    def login():
        global apiToken
        global apiKey
        url = "https://api.tagntrac.io/login?clientId=Tbocs0cjhrac"
        payload = json.dumps({
            "emailId": "{0}".format(id),
            "userSecret": "{0}".format(pwd),
        })
        headers = {
        'Origin': 'DOC.API',
        'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        rsp = json.loads(response.text)
        assert rsp['status'] == "SUCCESS", "login fail"
        fprint("Login as user: {0}".format(rsp['user']['userName']))
        apiToken = rsp['token']
        apiKey = rsp['clientApiKey']['clientId']
        return True    


class logger:
    def __init__(self, addr):
        self.addr = addr

    def initialize(self):
        self.status = False
        self.health = None

        self.command = None
        self.command_success = None
        self.command_cmd = None
        self.config = None
        self.config_endTime = None
        self.config_success = None
        self.lastResetAt = None
        self.state  = None
        self.err = None
        
    def getDeviceHealth(self):
        url = "https://api.tagntrac.io/device/{0}/health".format(self.addr)
        headers = {
            'x-api-key': '{0}'.format(apiKey)
        }
        response = requests.request("GET", url, headers=headers, data=payload)

        self.initialize()
        rsp = None

        try:
            rsp = json.loads(response.text)
            #
            #pprint.pprint(rsp)
        except Exception as e:
            fprint("ERR json load: " + response.text,)
            self.err  = 'errJson'
            return False

        if rsp is None:
            fprint("http rsp is None")
            self.err  = 'errRsp'
            return False
        
        if rsp["status"] != "SUCCESS":
            fprint("***ERR HTTP: {0} {1}".format(rsp["status"], response.reason))
            self.err  = 'errHttp'
            return False
        else:
            if 'health' in rsp['device']:
                self.health = rsp["device"]["health"]
                if 'config' in self.health:
                    self.config = self.health['config']
                    self.config_endTime = self.config['endTime']
                if 'command' in self.health:
                    self.command = self.health['command']
                    self.command_cmd = self.command['cmd']
                    if 'success' in self.command:
                        self.command_success = self.command['success']
                if 'lastResetAt' in self.health:
                    temp = self.health['lastResetAt']
                    temp = datetime.datetime.strptime(temp,'%Y-%m-%dT%H:%M:%S.%fZ')
                    self.lastResetAt = (temp - datetime.datetime(1970,1,1)).total_seconds()
            self.status = "SUCCESS"
            return True

    def updateBLEGatewayConfig(self,gwId, cmd):
        url = "https://api.tagntrac.io/device/{0}/shadow".format(gwId)
        headers = {
            'Authorization': '{0}'.format(apiToken),
            'Content-Type': 'application/json'
        }
        if cmd == 'read':
            payload = json.dumps({
                "ble_cmds": [{
                #"addr": "{0}".format(self.addr),
                #"cmd": "read"
                "addrs": this,
                "payload": "030702"
                }]})
        elif cmd == 'reset': 
            payload = json.dumps({
                "ble_cmds": [{
                "addr": "{0}".format(self.addr),
                "cmd": "reset",
                "payload": {
                    "tempInterval": 15, 
                    "advInterval": 4,
                    "startDelay": 0
                    }
                }]})
        elif cmd == 'configAndReset' :
            payload = json.dumps({
                "ble_cmds": [{
                "addr": "{0}".format(self.addr),
                "cmd": "configAndReset",
                "payload": {
                    "profileId": 0,
                    "tempInterval": 15,
                    "advInterval": 4,
                    "startDelay": 0
                    }
                }]})
        elif cmd == 'readAndReset' :
            payload = json.dumps({
            "ble_cmds": [{
                "addr": "{0}".format(self.addr),
                "cmd": "raw",
                "payload": {
                    "bytes": "0307020C050B000000000F01030000" #readAndReset
                    }
                }]})
        elif cmd =='alert':
            payload = json.dumps({
                "ble_cmds": [{
                "addr": "{0}".format(self.addr),
                "cmd": "alert",
                "payload": {
                    "version": "1.7.x",         #version >1.7.x
                    "lowTempAlert": 0.0,        #loT
                    "highTempAlert": 25.0,      #HiT
                    "consecutiveTempAlert": 1,  #
                    "lifetimeTempAlert": 0,     #1 enable
                    "startDelay": 3,            #2 activeTempInt
                    "stopDelay": 0,
                    "ignoreStart": 3,
                    "btnPressTime": 3,
                    "startBlinks": 3,
                    "stopGoodBlinks": 3,
                    "stopBadBlinks": 5,
                    "blinkLongMs": 500,
                    "blinkLongMsOff": 500,
                    "blinkShortMs": 250,
                    "blinkSHortMsOff": 250,
                    "activeTmpInt": 1,
                    "tripDuration": 576,          #trip (8+1)*actieTempInt
                    "lifetimeLowTemp": 0,
                    "lifetimeHighTemp": 25        #8.0
                    }
                }]})
        elif cmd == 'config' :
            payload = json.dumps({
            "ble_cmds": [{
                "addr": "{0}".format(self.addr),
                "cmd": "raw",
                "payload": {
                    "bytes": "0307020C050B000000000F01030000" #configure 
                    }
                }]})            
        print(this)
        response = requests.request("POST", url, headers=headers, data=payload)

        self.initialize()

        if response.ok is True:
            rsp = json.loads(response.text)
            if rsp['status'] == 'SUCCESS':
                self.status = 'SUCCESS'
                #self.state  = rsp['state']
                fprint("Sent {0} cmd".format(cmd))
                return True
            else:
                fprint("Sent {0} cmd not succussful".format(cmd))
                return False
        else:
            fprint("ERR: {0} cmd fail:  {1}".format(cmd, response.reason))
            return False

        

    def chkHealth(self):

        if self.health is None:
            fprint("no Health field")
            return False


        if 'config' not in self.health: 
            fprint("******ERR: no config in health")
            return True
        
        #fprint(self.health['config'])

        delta = time.time()-self.health['config']["endTime"]
        if delta > 50:
            fprint("******ERR: endTime: {0} seconds ago".format(int(delta)))
        else:
            fprint()

        if "vbat" in self.health.keys() and self.health["vbat"] < 2900: 
            fprint("******ERR vbat low: {0}".format(self.health["vbat"]))
            #return False
        if 'lastResetAt' in self.health:
            fprint("***lastReset at {0}".format(self.health['lastResetAt']))
        else:
            fprint("** no LastReset field")



        #try: 
        #    print("CFG: State: {0} Logsize:{1}, Intervals:{2} {3}, Alert:{4} {5} {6} Life:{7} {8} {9} Dur:{10}".format(
        #        self.health['config']['alertState'], self.health['config']['logSize'], 
        #        self.health['config']['interval'], self.health['config']['activeInterval'], 
        #        self.health['config']['alertLowTemp'],  self.health['config']['alertHighTemp'], self.health['config']['alertThreshold'],
        #        self.health['config']['alertLifetimeLowTemp'],  self.health['config']['alertLifetimeHighTemp'], 
        #            self.health['config']['alertLifetimeThreshold'], self.health['config']['alertTripDuration']))
        #except:
        #    print("CFG:  Logsize:{0}, Intervals:{1} {2}".format(
        #        self.health['config']['logSize'], 
        #        self.health['config']['interval'], self.health['config']['activeInterval']))
        #    pass


outFile = open('c:\\Users\\tagnt\\Downloads\\tnt-testg\\junk\\{0}_{1}_{2}.log'.format(GW,name_devlist,int(time.time())), 'a')
#outFile = sys.stdout

def fprint(*message):
    print(*message)
    print(*message,file=outFile)
    outFile.flush()


if __name__=="__main__":

    test_start = time.time()
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


    addlist = []
    alist = []
    addr_list = []
    for devlist in fname_devlist:
        with open(f'c:\\Users\\tagnt\\Downloads\\tnt-testg\\{devlist}', 'r') as fname:
            dev_list = fname.read().splitlines()
        addr_list.extend(dev_list)

    for i in range(0, len(addr_list), 4):
        addlist = addr_list[i:i+4]
        alist.append(addlist)


    addr_list = addr_list[:]
    #addr_list = addr_list[78:list_size]
 
    #random.shuffle(addr_list)
    #list_size = 500
    #addr_list = random.sample(addr_list,list_size)
##    addr_list = ['C46A7CF90010','C46A7CF90011','C46A7CF90012','C46A7CF90013',
##                 'C46A7CF90014','C46A7CF90015',
##                 'C46A7CF90016','C46A7CF90017']

    #addr_list =['C46A7CF90BE9']
    
    #endtime_list = [-1]*list_size
    #trial_list   = [-1]*list_size
    #stat_list  = ['None']*list_size
    data = []
    failed_list = []

    apiUser.login()
    fprint("\n\n>>>>>>>>>>>>>>>>>>>>>")
    fprint(str(datetime.datetime.now()))
    fprint("Gateway: ", GW, )
    #print(str(datetime.datetime.now()), file=outFile)
    #print("Gateway: ", GW, fname_devlist,file=outFile, flush=True)


    session_init=time.time()

    
    for index in range(list_size):
        
        #dev = addr_list[index]
        this = alist[int(index/4)]
        print(this)
        dev = alist[int(index/4)][index%4]
        # every two hour to acquire a credential 
        if time.time() - session_init > 3600:
            apiUser.login()
            session_init = time.time()
            fprint("******reconnect to {0}".format(id_inv))

        loggerDev = logger(dev)
        stat = 'err'
        healthStatus = False
        for i_cycle in range(cycle):
            if healthStatus is True:
                continue
            time.sleep(i_cycle*20)
                
            fprint("=======",dev,index+1,i_cycle+1 ,time.asctime())
            
            #loggerDev = logger(dev)

            if cmd == 'gethealth':
                #if loggerDev.getHealth() is False: continue
                loggerDev.getHealth()
                loggerDev.chkHealth()

            elif cmd =='alert':
                loggerDev.updateBLEGatewayConfig(GW,'alert')
                if loggerDev.status == 'SUCCESS' :
                    startTime = time.time()
                    delay = 0
                    while healthStatus is False and delay < maxDelay:
                        time.sleep(3)
                        delay += 3
                        loggerDev.getDeviceHealth()
                        if loggerDev.command_success:
                            healthStatus = True
                            stat = 'success'
                            
                            lastReset=loggerDev.lastResetAt-startTime
                            fprint("INFO:  lastReset {0:.0f} seconds".format(lastReset))
                            break
                
                    fprint(healthStatus, stat)
                    if stat == 'success':
                        data.append([dev,'connect'+str(i_cycle+1), stat, time.time() - startTime])
                        fprint("INFO: lastReset status {0} time: {1} seconds".format(healthStatus, time.time() - startTime))


            elif cmd == 'reset':
                loggerDev.updateBLEGatewayConfig(GW,'reset')
                if loggerDev.status == 'SUCCESS' :
                    startTime = time.time()
                    delay = 0
                    
                    while healthStatus is False and delay < maxDelay:
                        time.sleep(3)
                        delay += 3
                        loggerDev.getDeviceHealth()
                        if loggerDev.command_success:
                            healthStatus = True
                            stat = 'success'
                            
                            lastReset=loggerDev.lastResetAt-startTime
                            fprint("INFO:  lastReset {0:.0f} seconds".format(lastReset))
                            break
                
                    fprint(healthStatus, stat)
                    if stat == 'success':
                        data.append([dev,'connect'+str(i_cycle+1), stat, time.time() - startTime])
                        fprint("INFO: lastReset status {0} time: {1} seconds".format(healthStatus, time.time() - startTime))

            elif cmd == 'configAndReset':
                loggerDev.updateBLEGatewayConfig(GW,'configAndReset')
                if loggerDev.status == 'SUCCESS' :
                    startTime = time.time()
                    delay = 0
                    
                    while healthStatus is False and delay < maxDelay:
                        time.sleep(3)
                        delay += 3
                        loggerDev.getDeviceHealth()
                        if loggerDev.command_success:
                            healthStatus = True
                            stat = 'success'
                            
                            lastReset=loggerDev.lastResetAt-startTime
                            fprint("INFO:  lastReset {0:.0f} seconds".format(lastReset))
                            break
                
                    fprint(healthStatus, stat)
                    if stat == 'success':
                        data.append([dev,'connect'+str(i_cycle+1), stat, time.time() - startTime])
                        fprint("INFO: lastReset status {0} time: {1} seconds".format(healthStatus, time.time() - startTime))
                 
            elif cmd == 'read':
                loggerDev.updateBLEGatewayConfig(GW,'read')
                if loggerDev.status == 'SUCCESS':
                    startTime = time.time()

                    #sleep 5s
                    time.sleep(5)
                    healthStatus = False
                    stat = 'errTimeout'
                    delay = 0
                
                    cmdFailCount = 0
                    # either endtime<100 or success=true
                    while not healthStatus and delay < maxDelay:
                        time.sleep(3)
                        delay += 3
                        loggerDev.getDeviceHealth()
                        if loggerDev.config_endTime != None:
                            delta = time.time()-loggerDev.config_endTime
                            if delta < 100:
                                fprint("endTime changed: {0} seconds ago".format(int(delta)))
                                healthStatus = True
                                stat = 'success_norsp'
                                if loggerDev.command_success == True:
                                    stat = 'success'
                                break
                            else:
                                fprint("***INF: no endTime change")
                    
                    fprint(healthStatus, stat)

                    if stat == 'success' or stat == 'success_norsp':
                        #endtime_list[index] = time.time() - startTime
                        data.append([dev, 'connect'+str(i_cycle+1),stat, time.time() - startTime])
                                          
                        fprint("INFO:  {0} time: {1:.0f} seconds".format(stat, ((time.time() - startTime))))
                    
                loggerDev.chkHealth()

            df = pd.DataFrame(data, columns=['addr', 'trial','stat', 'delay'])
            fprint('<=50s:\t',len(df[df['delay']<=50]))
            fprint('<=100s:\t',len(df[df['delay']>50]))
            fprint(df.stat.value_counts())
            fprint(df.trial.value_counts())
            fprint(df.describe())

    fprint('test lasts: ',time.time()-test_start) 
    assert len(data)>= len(addr_list)*0.7

