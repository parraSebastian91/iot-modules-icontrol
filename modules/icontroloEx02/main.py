# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE file in the project root for
# full license information.
import os
import asyncio
import random
import logging
import json
import threading
import signal
import time


from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device import Message, MethodResponse
from datetime import timedelta, datetime
from utils.lcd_functions import lcd_string, lcd_init
from utils.telemetry import *
import asyncio
from dotenv import load_dotenv

stop_event = threading.Event()
logging.basicConfig(level=logging.DEBUG)


def create_client():
    client = GetgetConnectionHub()
    #Orquestador de Mensajes
    def message_handler(message):
        lcd_string(message.input_name, 1)
        if message.input_name == "input1":
            lcd_string(message.custom_properties, 2)
        elif message.input_name == "input2":
            lcd_string(message.custom_properties, 2)
        else:
            lcd_string('unknown input', 1)
            lcd_string('xD', 2)

    # Define behavior for receiving a twin desired properties patch
    # NOTE: this could be a coroutine or function
    def twin_patch_handler(patch):
        print("the data in the desired properties patch was: {}".format(patch))

    # Orquestador de Metodos
    async def method_handler(method_request):
        logging.info('Method Handler Inicio')
        logging.info(method_request.name)
        if method_request.name == "get_data":
            logging.info(method_request.payload)
            lcd_string(method_request.payload, 1)
            method_response = MethodResponse.create_from_method_request(
                method_request, 200, "some data"
            )
            await client.send_method_response(method_response)
        else:
            print("Unknown method request received: {}".format(method_request.name))
            method_response = MethodResponse.create_from_method_request(
                method_request, 400, None)
            await client.send_method_response(method_response)

    # Se asigna los orquestadores al objeto Cliente IoT Edge
    client.on_message_received = message_handler
    client.on_twin_desired_properties_patch_received = twin_patch_handler
    client.on_method_request_received = method_handler

    return client


async def run(client):
    # Customize this coroutine to do whatever tasks the module initiates
    # e.g. sending messages
    await client.connect()
    while not stop_event.is_set():
        lcd_string('Waiting orders...', 1)
        await asyncio.sleep(1000)


def main():
    load_dotenv()
    client = create_client()
    lcd_init()
    lcd_string('Iniciando', 1)
    time.sleep(3)
    lcd_string('3 segundos ...', 2)
    time.sleep(3)

    def module_termination_handler(signal, frame):
        print("IoTHubClient sample stopped by Edge")
        stop_event.set()

    # Set the Edge termination handler
    signal.signal(signal.SIGTERM, module_termination_handler)

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(run(client))
    except Exception as e:
        print("Unexpected error %s " % e)
        raise
    finally:
        print("Shutting down IoT Hub Client...")
        loop.run_until_complete(client.shutdown())
        loop.close()


if __name__ == "__main__":
    main()
