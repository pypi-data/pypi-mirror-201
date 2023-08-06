#!/usr/bin/env python
from pprint import pprint
import websockets
from uuid import uuid4
import json
import asyncio
import math
from .binvox import Binvox
from PIL import Image
from numpy import asarray
from .palette import palette

from sklearn.neighbors import NearestNeighbors
import numpy as np

color_wheel = [
    ['Purple wool'          , 'wool 10'                  , 'Purple'              , '764b73'],
    ['Magenta wool'         , 'wool 2'                   , 'Magenta'             , 'a05077'],
    ['Pink wool'            , 'wool 6'                   , 'Pink'                , 'ce747e'],
    ['Pink hardened Clay'   , 'stained_hardened_clay 6'  , 'dark pink'           , '9c544e'],
    ['Red hardened Clay'    , 'stained_hardened_clay 14' , 'dark reddish pink'   , '8d493e'],
    ['Red wool'             , 'wool 14'                  , 'dark reddish pink'   , '9d433b'],
    ['Red mushroom block'   , 'red_mushroom_block'       , 'dark Red'            , 'ab3335'],
    ['Redstone block'       , 'redstone_block'           , 'Red'                 , 'e54547'],
    ['Orange hardened clay' , 'stained_hardened_clay 1'  , 'dark reddish orange' , 'b63b34'],
    ['Orange wool'          , 'wool 1'                   , 'Orange'              , 'd45e42'],
    ['Yellow hardened clay' , 'stained_hardened_clay 4'  , 'Yellowish orange'    , 'ca893c'],
    ['Gold block'           , 'gold_block'               , 'yellow'              , 'e3cf52'],
    ['Yellow wool'          , 'wool 4'                   , 'Yellowish green'     , 'bea831'],
    ['Melon'                , 'melon_block'              , 'Dark green'          , '6c7525'],
    ['Lime wool'            , 'wool 5'                   , 'Green'               , '64940e'],
    ['Emerald block'        , 'emerald_block'            , 'Blue green'          , '53924b'],
    ['Green wool'           , 'wool 13'                  , 'Dark green'          , '3a4827'],
    ['Prismarine bricks'    , 'prismarine 1'             , 'Dark green blue'     , '415647'],
    ['Cyan wool'            , 'wool 9'                   , 'Cyan'                , '235f6a'],
    ['Packed ice'           , 'packed_ice'               , 'Light blue gray'     , '81929c'],
    ['Light blue wool'      , 'wool 3'                   , 'Light blue'          , '686997'],
    ['Lapis lazul block'    , 'lapis_block'              , 'Dark blue'           , '3b4664'],
    ['Blue wool'            , 'wool 1'                   , 'very dark blue'      , '464165'],
    ['Blue hardened clay'   , 'stained_hardened_clay 11' , 'Almost block blue'   , '51444d'],
]


class Client:
    def __init__(self, port=3000):
        self._port = port
        self._websocket = None
        self._send_queue = []
        self._awaiting_response = {}
        self._awaiting_limit = 90
        self._nn_model = None

    def _hex2rgb(self, h):
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    async def connect(self):
        uri = f"ws://0.0.0.0:{self._port}/script"
        self._websocket = await websockets.connect(uri)
        asyncio.ensure_future(self._monitor_responses())


    async def send_command(self, cmd):
        msg = {
            "header": {
                "version": 1,
                "requestId": str(uuid4()),
                "messageType": "commandRequest",
                "messagePurpose": "commandRequest",
            },
            "body": {
                "commandLine": cmd,
                "origin": {
                    "type": "player"
                }
            }
        }
        future = asyncio.get_event_loop().create_future()
        self._send_queue.append([msg, future])
        await self._consider_send_queue()
        return await future

    async def _monitor_responses(self):
        async for response_msg in self._websocket:
            response_msg = json.loads(response_msg)
            if response_msg.get('header').get('messagePurpose') == 'commandResponse':
                # ... and it's for an awaited command
                request_id = response_msg.get('header').get('requestId')
                if request_id in self._awaiting_response:
                    status = response_msg.get('body').get('statusCode')
                    # if status < 0:
                    #     import sys
                    #     print(f"fatal error {status}", file=sys.stderr)
                    # else:
                    #     future =  self._awaiting_response.get(request_id)
                    #     future.set_result(response_msg)
                    #     future.done()
                    future =  self._awaiting_response.get(request_id)
                    future.set_result(response_msg)
                    future.done()
                self._awaiting_response.pop(request_id)
                await self._consider_send_queue()
      #   // Print errors (if any)
      #   if (msg.body.statusCode < 0)
      #     console.log(awaitedQueue[msg.header.requestId].body.commandLine, msg.body.statusMessage)
      #   // ... and delete it from the awaited queue
      #   delete awaitedQueue[msg.header.requestId]
      # }
    # }



    async def _consider_send_queue(self):
        while len(self._send_queue) > 0 and len(self._awaiting_response) < self._awaiting_limit:
            item = self._send_queue.pop(0)
            import pprint
            pprint.pprint(item)
            msg =  item[0]
            future = item[1]
            self._awaiting_response[msg['header']['requestId']] = future
            print(f"Sending: {json.dumps(msg)}")
            await self._websocket.send(json.dumps(msg))
            # asyncio.ensure_future(self._recv_one_response())
            # await asyncio.sleep(0.1)
        # await self.websocket.send(json.dumps(msg))


    async def fill(self, x1, y1, x2, y2, material):
        pass

    async def draw_cyclinder(self, radius, height, material, x_offset=0, y_offset=0, z_offset=0):
        tasks = []
        for y in range(0, height):
            tasks.append(self.draw_circle(radius, material, x_offset=x_offset, y_offset=y + y_offset, z_offset=z_offset))
        results = await asyncio.gather(*tasks)


    async def draw_cone(self, radius, material, x_offset=0, y_offset=0, z_offset=0):
        tasks = []
        for y in range(0, radius):
            print(f"Runing draw_circle({radius-y}, {material}, {y + y_offset})")
            tasks.append(self.draw_circle(radius-y, material, x_offset=x_offset, y_offset=y + y_offset, z_offset=z_offset))
        results = await asyncio.gather(*tasks)

    async def draw_cube(self, x, y, size, material, hollow=False):
        pass

    async def draw_binvox(self, path, material, y_offset=0, x_offset=0, z_offset=0):
        model = Binvox.read(path, mode='dense').numpy()
        (depth, width, height) = model.shape

        tasks = []
        for x in range(0, depth):
            for z in range(0, width):
                for y in range(0, height):
                    if model[x][z][y] and (
                            x == 0
                            or x == depth - 1
                            or y == 0
                            or y == height - 1
                            or z == 0
                            or z == width - 1
                            or not model[x-1][z][y]
                            or not model[x+1][z][y]
                            or not model[x][z-1][y]
                            or not model[x][z+1][y]
                            or not model[x][z][y-1]
                            or not model[x][z][y+1]
                    ):
                        print(f"{x}, {y}, {z}")
                        tasks.append(self.send_command(f"setblock ~{x + x_offset} ~{y + y_offset} ~{z + z_offset} {material}"))

        results = await asyncio.gather(*tasks)

    async def draw_circle(self, radius, material, y_offset=0, x_offset=0, z_offset=0):
        tasks = []


        # # Figure out the key blocks we want to place
        # key_blocks = []
        # for x in range(0, radius+1):
        #     z = round(radius*math.sin(math.acos(x/radius)))
        #     key_blocks.append([x, y, z])
        #     key_blocks.append([x, y, -z])
        #     key_blocks.append([-x, y, z])
        #     key_blocks.append([-x, y, -z])

        # blocks = interpolate_blocks(key_blocks)

        last_z = None
        for x in range(0, radius+1):
            new_z = round(radius*math.sin(math.acos(x/radius)))
            zs = [new_z]
            if last_z:
                zs = range(new_z, last_z+1)

            for z in zs:
                tasks.append(self.send_command(f"setblock ~{x + x_offset} ~{y_offset} ~{z + z_offset} {material}"))
                tasks.append(self.send_command(f"setblock ~{x + x_offset} ~{y_offset} ~{-z + z_offset} {material}"))
                tasks.append(self.send_command(f"setblock ~{-x + x_offset} ~{y_offset} ~{z + z_offset} {material}"))
                tasks.append(self.send_command(f"setblock ~{-x + x_offset} ~{y_offset} ~{-z + z_offset} {material}"))
                
            last_z = new_z

        results = await asyncio.gather(*tasks)

    async def draw_monochrome_image(self, file, material="obsidian", background=None):
        image = Image.open(file)
        # convert image to numpy array
        data = asarray(image)
        height = data.shape[0]
        width = data.shape[1]
        channels = data.shape[2]

        tasks = []
        for x in range(0, width):
            for y in range(0, height):
                pixel = data[y][x]
                is_black = False
                for i in range(0, channels):
                    if pixel[i] != 255:
                        is_black=True
                        break

                if is_black:
                    tasks.append(self.send_command(f"setblock ~{x} ~{height-y} ~ {material}"))
                elif background is not None:
                    tasks.append(self.send_command(f"setblock ~{x} ~{height-y} ~ {background}"))

        await asyncio.gather(*tasks)

    def _build_nn_model(self):
        global palette
        X = np.array([x[1] for x in palette])
        # global color_wheel
        # X = np.array([self._hex2rgb(x[3]) for x in color_wheel])
        # self._nn_model = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit(X)
        self._nn_model = NearestNeighbors(n_neighbors=1, algorithm='kd_tree').fit(X)

    async def draw_image_nn(self, file):
        global color_wheel
        image = Image.open(file)
        # convert image to numpy array
        data = asarray(image)
        height = data.shape[0]
        width = data.shape[1]
        channels = data.shape[2]

        if self._nn_model is None:
            self._build_nn_model()
        nbrs = self._nn_model

        tasks = []
        for y in range(height):
            distances, indices = nbrs.kneighbors(data[y])
            # materials = [color_wheel[i[0]][1] for i in indices]
            materials = [palette[i[0]][0] for i in indices]
            # print(f"material size is {len(materials)}")
            for x in range(width):
                tasks.append(self.send_command(f"setblock ~{x} ~{height-y} ~ {materials[x]}"))

        await asyncio.gather(*tasks)

    async def draw_palette(self):
        global palette
        tasks = []
        for i in range(len(palette)):
            tasks.append(self.send_command(f"setblock ~+{i} ~ ~ {palette[i][0]}"))
        await asyncio.gather(*tasks)



    async def draw_image(self, file):
        image = Image.open(file)
        # convert image to numpy array
        data = asarray(image)
        height = data.shape[0]
        width = data.shape[1]
        channels = data.shape[2]

        tasks = []
        for x in range(0, width):
            for y in range(0, height):
                pixel = data[y][x]

                material = self._closest_block_for_color(pixel)
                tasks.append(self.send_command(f"setblock ~{x} ~{height-y} ~ {material}"))

        await asyncio.gather(*tasks)

    async def build_pyramid(self, size, material='glowstone'):
        tasks = []
        for y in range(0, size+1):
            side = size - y
            for x in range(-side, side+1):
                tasks.append(self.send_command(f"setblock ~{x} ~{y} ~{-side} {material}"))
                tasks.append(self.send_command(f"setblock ~{x} ~{y} ~{+side} {material}"))
                tasks.append(self.send_command(f"setblock ~{-side} ~{y} ~{x} {material}"))
                tasks.append(self.send_command(f"setblock ~{+side} ~{y} ~{x} {material}"))
        await asyncio.gather(*tasks)

    def _closest_block_for_color(self, rgb):
        global color_wheel
        closest_block = None
        closest_distance = None
        # print(f"Finding closest block for point {rgb}")
        for color_record in color_wheel:
            rgb2 = self._hex2rgb(color_record[3])
            distance = math.sqrt((rgb[0]-rgb2[0])**2 + (rgb[1]-rgb2[1])**2 + (rgb[2]-rgb2[2])**2)
            if closest_block is None or distance < closest_distance:
                closest_distance = distance
                closest_block = color_record[1]

        return closest_block

    async def draw_sphere(self, radius, material):
        tasks = []

        for y in range(radius):
            segment_radius = round(math.sqrt(radius**2 - y**2))
            tasks.append(self.draw_circle(segment_radius, material, y))
            tasks.append(self.draw_circle(segment_radius, material, -y))

        results = await asyncio.gather(*tasks)
