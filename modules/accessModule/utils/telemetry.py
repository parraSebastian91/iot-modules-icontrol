from config.config import getConnStrDevice
import json
from azure.iot.device.aio import IoTHubDeviceClient, IoTHubModuleClient
from azure.iot.device import Message, MethodResponse


def GetgetConnectionHub():
    conn_str = getConnStrDevice()     
    return IoTHubDeviceClient.create_from_connection_string(conn_str)

async def sendTelemetry(device_client, telemetry_msg):
    msg = Message(json.dumps(telemetry_msg))
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    await device_client.send_message(msg)

def GetConnectionFromEdgeEnviroment():
    return IoTHubModuleClient.create_from_edge_environment()