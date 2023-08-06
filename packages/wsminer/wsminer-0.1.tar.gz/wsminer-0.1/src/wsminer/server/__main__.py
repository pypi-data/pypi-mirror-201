#!/usr/bin/env python

import re
import asyncio
import websockets
import json
from uuid import uuid4
import socket
import pprint

minecraftWebsocket = None
scriptWebsockets = set()


def registerScript(websocket):
    global scriptWebsockets
    scriptWebsockets.add(websocket)

def registerMinecraft(websocket):
    global minecraftWebsocket
    minecraftWebsocket = websocket


# On Minecraft, when you type "/connect localhost:3000" it creates a connection
async def mineproxy(websocket, path):
    global minecraftWebsocket, scriptWebsocket
    print("Connection to " + path + "\n")

    if "script" in path:
        registerScript(websocket)
        try:
            async for message in websocket:
                print(f"Received message from script: {message}")
                if minecraftWebsocket is not None:
                    print("Relaying the message\n")
                    await minecraftWebsocket.send(message)
        except websockets.exceptions.ConnectionClosedError:
            print("Script websocket connection closed\n")
            scriptWebsockets.remove(websocket)

    else:
        registerMinecraft(websocket)
        async for message in websocket:
            print(f"Received and discarding message from minecraft: {message}")

            closed_web_sockets = []
            for scriptWebsocket in scriptWebsockets:
                try:
                    await scriptWebsocket.send(message)
                except websockets.exceptions.ConnectionClosedError:
                    print("Received script disconnect\n")
                    closed_web_sockets.append(scriptWebsocket)

            for scriptWebsocket in closed_web_sockets:
                scriptWebsockets.remove(scriptWebsocket)

    # if minecraftWebsocket is None:
    #     minecraftWebsocket = websocket
    #     print('Minecraft connected')
    # else:
    #     scriptWebsocket = websocket
    #     print('Script connected')

    # # Tell Minecraft to send all chat messages. Required once after Minecraft starts
    # await websocket.send(
    #     json.dumps({
    #         "header": {
    #             "version": 1,                     # We're using the version 1 message protocol
    #             "requestId": str(uuid4()),        # A unique ID for the request
    #             "messageType": "commandRequest",  # This is a request ...
    #             "messagePurpose": "subscribe"     # ... to subscribe to ...
    #         },
    #         "body": {
    #             "eventName": "PlayerMessage"
    #         },
    #     }))

    # print("Awaiting message\n")
    # async for message in websocket:
    #     print("Received message: ")
    #     pprint.pprint(message)

    # print("Done waiting for messages\n")


    # def send(cmd):
    #     # TODO
    #     pass

    # # def draw_pyramid(size):
    # #     # TODO
    # #     pass

    # # try:
    # #     # When MineCraft sends a message (e.g. on player chat), print it.
    # #     async for msg in websocket:
    # #         msg = json.loads(msg)
    # #         if msg['body']['eventName'] == 'PlayerMessage':
    # #             match = re.match(r'^pyramid (\d+)', msg['body']['properties']['Message'],
    # #                              re.IGNORECASE)
    # #             if match:
    # #                 draw_pyramid(int(match.group(1)))
    # # except websockets.exceptions.ConnectionClosedError:
    # #     print('Disconnected from MineCraft')


start_server = websockets.serve(mineproxy, host="0.0.0.0", port=3000)

host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(f'Ready. On MineCraft chat, type /connect {host_ip}:3000')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
