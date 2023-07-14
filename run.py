import time
import struct
import sys
import ssl
import json
import datetime
import psycopg2
import requests
import datetime

apiToken = None
apiKey = None
id = "qdemo@tagntrac.com"
pwd = 
url = "https://api.staging.tagntrac.io/v2/loggers/schedule/command"


loggers = [{"deviceId": "C46A7CF96BA0",
        "command":"uploadAndReset",
        "profile": 1,
        "project" : "LOGGER",
        "deprovision" : False,
        "lookback_hours" : 24
        }, {"deviceId": "C46A7CF963E1",   
        "command":"uploadAndReset",
        "profile": 1,
        "project" : "LOGGER",
        "deprovision" : True,
        "lookback_hours" : 24}]

headers = {
        "Authorization": "",
        "Content-Type": "application/json"
    }

payload = {
    "webhooks": ["https://webhook.site/ca160ddf-77c6-4f00-9ec3-78262009eefb"], 
        "site": "TNT_Campbeel",
        "zone": "z-T32224",
        "type": "append",
        "loggers": loggers
}
print("\n\n>>>>>>>>>>>>>>>>>>>>>")
print(str(datetime.datetime.now()))
response = requests.request("Post", url, headers=headers, data=payload)
rsp = json.loads(response.text)
print(rsp)


