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
url = "https://api.staging.tagntrac.io/v2/loggers/schedule/command"


#caPath = "C:\Users\tagnt\Downloads\AmazonRootCA1.pem"
#certPath = "C:\Users\tagnt\Downloads\certificate.pem.crt"
#keyPath = "C:\Users\tagnt\Downloads\private.pem.key"

#class apiUser:
    #def __init__(self, id, pwd):
       # self.id = id
       # self.pwd = pwd

#    def login():
#        global apiToken
#        global apiKey
 #       url = "https://api.staging.tagntrac.io/v2/login"
  #      payload = json.dumps({
   #         "emailId": "{0}".format(id),
    #        "userSecret": "{0}".format(pwd),
     #   })
      #  headers = {
     #   'Origin': 'DOC.API',
      #  'Content-Type': 'application/json'
       # }
       # response = requests.request("POST", url, headers=headers, data=payload)
        #rsp = json.loads(response.text)
        #assert rsp['status'] == "SUCCESS", "login fail"
        #print("Login as user: {0}".format(rsp['user']['userName']))
        #apiToken = rsp['token']
        #apiKey = rsp['clientApiKey']['clientId']
        #return True    

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
        "Authorization": "eyJraWQiOiJES2hWMklkWVRCRm1XWldoblh1OG1PTHhtS0Z2Ukg0dHRoZnorQURNSEZNPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJjN2YyODRhZC1kMzk1LTQyMjktYmZmZC02NzRkNWM4MmM2YzIiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLnVzLWVhc3QtMS5hbWF6b25hd3MuY29tXC91cy1lYXN0LTFfY0JrVUJPcXRmIiwiY29nbml0bzp1c2VybmFtZSI6ImM3ZjI4NGFkLWQzOTUtNDIyOS1iZmZkLTY3NGQ1YzgyYzZjMiIsImF1ZCI6IjFhamsyNjkyY2FnbTdmazJpNWhjNDkxOGl0IiwiZXZlbnRfaWQiOiI2NjRmMjAxYi0xNzdkLTQ3YWMtYTJkZC0zMTJhM2YxOTNlYWMiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY4OTYxNzQ3NCwiZXhwIjoxNjg5NjQ2Mjc0LCJjdXN0b206cGVybWlzc2lvbnMiOiJtYW5hZ2U6b3JnYW5pemF0aW9uLCBtYW5hZ2U6dXNlcnMsIGNyZWF0ZTp3ZWJob29rLCByZWFkOndlYmhvb2ssIHVwZGF0ZTp3ZWJob29rLCBkZWxldGU6d2ViaG9vaywgY3JlYXRlOnJ1bGUsIHJlYWQ6cnVsZSwgdXBkYXRlOnJ1bGUsIGRlbGV0ZTpydWxlLCByZWFkOmRhdGFUcmFpbCwgY3JlYXRlOmdlb2ZlbmNlLCByZWFkOmdlb2ZlbmNlLCB1cGRhdGU6Z2VvZmVuY2UsIGRlbGV0ZTpnZW9mZW5jZSwgY3JlYXRlOmFzc2V0VHlwZSwgcmVhZDphc3NldFR5cGUsIHVwZGF0ZTphc3NldFR5cGUsIGRlbGV0ZTphc3NldFR5cGUsIGNyZWF0ZTpzaXRlLCByZWFkOnNpdGUsIHVwZGF0ZTpzaXRlLCBkZWxldGU6c2l0ZSwgY3JlYXRlOnByb2plY3QsIHJlYWQ6cHJvamVjdCwgdXBkYXRlOnByb2plY3QsIGRlbGV0ZTpwcm9qZWN0LCBwcm92aXNpb246ZGV2aWNlLCBwcm92aXNpb246Z2F0ZXdheSwgZGVwcm92aXNpb246ZGV2aWNlLCBkZXByb3Zpc2lvbjpnYXRld2F5LCBwcm92aXNpb246cHJpbnRlciwgZGVwcm92aXNpb246cHJpbnRlciwgY3JlYXRlOnpwbCwgcmVhZDp6cGwsIHVwZGF0ZTp6cGwsIGRlbGV0ZTp6cGwsIGNyZWF0ZTp6b25lLCB1cGRhdGU6em9uZSwgcmVhZDp6b25lLCBkZWxldGU6em9uZSIsImlhdCI6MTY4OTYxNzQ3NCwiZW1haWwiOiJpbnZlbnRvcnlAdGFnbnRyYWMuaW8ifQ.BRgF7SCqtl2J-urIezltcPoD5ylKDymlXp9v85c4M3S86TNNZF6S8VPWmHyvrmvRsChasSdTOau76-d7VVCMshDCNwTCwYO1YrSFq0i9yK6GnZX0omGWNAfsI4Y4EMyi7_W4BSS4a9XfUbSL4QzFxrjEOdYeki0m4c_kykQWBswv9WJFBnVsXLUeph3crREN7gq_Of9-thVlNCT1RppEURH9oUQWWs7odJMgoeR-MM3irUyzudOLBOSMkFi1lURBOcENZRe_Jcv4ZCWQVvIZe1p6ndQWjCN44u5tPygnKWZEZEukkUyP0QW4VPtjgUN3UYX7e7TTl2cR_ykTxJtSFQ",
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


