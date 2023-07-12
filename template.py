import paho.mqtt.client
import time
import struct
import queue
import sys
import ssl
import json
import datetime
import psycopg2
import requests
import datetime
import random


apiBaseUrl = "https://api.tagntrac.io/device/v2/loggers/schedule/command"
idToken = " "
#type = ["new", "append"]
#command = ["uploadAndReset, upload, reset, healthcheck, configureAndReset"]
webhook = "https://webhook.site/ca160ddf-77c6-4f00-9ec3-78262009eefb"
class Logger:
    def __init__(self, deviceId, command, profile, project, deprovision, lookback_hours):
        self.deviceId = deviceId
        self.command = command
        self.profile = profile
        self.project = project
        self.deprovision = deprovision
        self.lookback_hours = lookback_hours

loggers = []
commands = []

class Gateway:
    def __init__(self, site, zone):
        self.site = site
        self.zone = zone

def send_webhooks(webhooks, Gateway, Type, Logger,id):
    for webhook in webhooks:
        payload = {
            "webhooks": "https://webhook.site/ca160ddf-77c6-4f00-9ec3-78262009eefb", 
            "site": Gateway.site,
            "zone": Gateway.zone,
            "type": Type,
            "command_array": get_logger_metadata(Logger)

        }
        headers = {
            "Authorization": id,
            "Content-Type": "application/json"
        }
        response = requests.post(webhook, json=payload, headers=headers)
        
def get_logger_metadata(loggers):
    logger_metadata = []
    for logger in loggers:
        metadata = {
            "deviceId": logger.deviceId,
            "command": logger.command,
            "profile": logger.profile,
            "project": logger.project,
            "deprovision": logger.deprovision,
            "lookback_hours": logger.lookback_hours
        }
        logger_metadata.append(metadata)
    return logger_metadata



def process_schedule_command(apiBaseUrl, idToken, webhooks, Gateway, type, loggers):

    organizationId = get_organization_id_from_token(idToken)


    loggers_data = get_logger_metadata(loggers)

 
    if not loggers_data:
        return {"error": "None of the loggers belong to the organization."}
    ble_cmd = []
    ble_cmds = {
                "site": Gateway.site,
                "zone": Gateway.zone,
                "type": type,
              }   
    current_time = datetime.datetime.now()
    for logger in loggers_data:
        last_uploaded = logger.lastUploadedAt
        time_diff = current_time - last_uploaded
        if time_diff.seconds()/3600 <= logger.lookback_hours:
            ble_cmd.append(get_logger_metadata(logger))
    ble_cmds.append(ble_cmd)

    #  The deprovision field and project field is checked if the logger is to be only deprovisioned or reassigned to other project and appropriate action is taken.
    for logger in loggers:
        if logger.deprovision:
            deprovision_logger(logger)
        else:
            reassign_logger(logger)

    #  Gateways belonging to the site/zone are fetched from RDS.
    gateways = get_gateways(Gateway.site, Gateway.zone)

    #  Shadow of each gateway is fetched from AWS-IoT Core.
    for gateway in gateways:
        shadow = get_gateway_shadow(gateway)

        #  If the type field is new, then the previously created ble_cmds array is added to the desired object and the shadow of all gateways is updated.
        if type == "new":
            if "desired" not in shadow:
                shadow["desired"] = {}
            shadow["desired"]["ble_cmds"] = ble_cmds
        #If the type field is not new and have some other value, the previously created ble_cmds array is appended to the already 
        # available ble_cmds array in the desired object of the shadow and the shadow is then updated with modified desired object.
        else:
            if "" not in shadow:
                shadow[""] = {}
            if "ble_cmds" not in shadow[""]:
                shadow[""]["ble_cmds"] = []
            shadow[""]["ble_cmds"].extend(ble_cmds)

        #  All webhook URLs in the webhook array are fired with newly updated desired object of the gateway shadow.
        send_webhooks(webhooks, shadow[""])

    return {"success": True}

# Helper functions

def get_organization_id_from_token(idToken):
    # Replace with your implementation to extract organizationId from the idToken
    return "your_organization_id"

def deprovision_logger(logger):
    # Replace with your implementation to perform deprovisioning action for the logger
    print(f"Deprovision logger: {logger['deviceId']}")

def reassign_logger(logger):
    # Replace with your implementation to perform reassignment action for the logger to another project
    print(f"Reassign logger: {logger['deviceId']}")

def get_gateways(site, zone):
    # Replace with your implementation to fetch gateways from RDS based on site/zone
    gateways = []
    # Query RDS to get gateways
    gateway = Gateway(site="", zone="")
    gateways.append(gateway)
    return gateways

def get_gateway_shadow(gateway):
    # Replace with your implementation to fetch the gateway shadow from AWS-IoT Core
    shadow = {
        "desired": {}
    }
    # Query AWS-IoT Core to get the shadow
    return shadow

response = process_schedule_command(apiBaseUrl, idToken, ["https://webhook.site/ca160ddf-77c6-4f00-9ec3-78262009eefb"], "TNT_Campbeel", "z-T32224", "append", loggers)
print(response)