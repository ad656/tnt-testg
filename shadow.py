import json
import requests
import datetime
import subprocess
import time

apiToken = None
apiKey = None

id_inv = "inventory@tagntrac.io"
pwd_inv = "T6wkccwd#1"

id = id_inv
pwd = pwd_inv
GW = 'GWT53488'
url = "https://api.tagntrac.io/device/{0}/shadow".format(GW)

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
        print("Login as user: {0}".format(rsp['user']['userName']))
        apiToken = rsp['token']
        apiKey = rsp['clientApiKey']['clientId']
        #print(response.text)
        #print(json.loads(response.text))
        #print(type(response.text))
        return True    

header = {
        "Authorization": apiToken,
        "Content-Type": "application/json"
}

payload = json.dumps({
        "ble_cmds": 
        {
            "addrs": ["C46A7CF90FAE",
                    "C46A7CF9CACD",
                    "C46A7CF9D008",
                    "C46A7CF9D066"],
            "payload": "030702"
        }
    
})

def runcmd():
    print("running gw_monitor on " + GW)
    result = subprocess.run(["python", "gw_monitor.py"], stdout=subprocess.PIPE, text=True)

    # Write the captured output to "out.txt" manually
    with open("out.txt", "w") as outfile:
        outfile.write(result.stdout)


print(datetime.datetime.now())
login()
runcmd()
response = requests.post(url,headers = header, data = payload)

rsp = json.loads(response.text)
print(rsp)


