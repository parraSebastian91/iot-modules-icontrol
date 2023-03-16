# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
import os
import asyncio
import random
import logging
import json

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device import Message, MethodResponse
from datetime import timedelta, datetime
from utils.lcd_functions import lcd_string, lcd_init
from utils.telemetry import *
import asyncio
from dotenv import load_dotenv


async def devolverSaludos():
    return "hola de vuelta"


async def main():
    load_dotenv()
    conn_client = GetgetConnectionHub()
    await conn_client.connect()
    lcd_init()

    async def method_request_handler(method_request):
        # Determine how to respond to the method request based on the method name
        if method_request.name == "method1":
            # set response payload
            payload = {"result": True, "data": "some data"}
            status = 200  # set return status code
            print("executed method1")
        elif method_request.name == "method2":
            # set response payload
            payload = {"result": True, "data": 1234}
            status = 200  # set return status code
            print("executed method2")
        else:
            # set response payload
            payload = {"result": False, "data": "unknown method"}
            status = 400  # set return status code
            print("executed unknown method: " + method_request.name)
        
        # Send the response
        method_response = MethodResponse.create_from_method_request(method_request, status, payload)
        await conn_client.send_method_response(method_response)

    # Set the method request handler on the client
    conn_client.on_method_request_received = method_request_handler

        # Define behavior for halting the application
    contador = 0

    async def stdin_listener():
        while True:
            lcd_string('Saludos ' + str(contador), 1)
            await sendTelemetry(conn_client,  {"saludos": 'Saludos' + str(contador)})
            contador = contador + 1
            await asyncio.sleep(8)

    loop = asyncio.get_running_loop()
    await loop.run_forever(None, stdin_listener)
    # Finally, shut down the client
    await conn_client.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
