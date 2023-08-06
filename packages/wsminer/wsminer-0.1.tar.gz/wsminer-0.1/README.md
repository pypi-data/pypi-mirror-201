# wsminer
Minecraft Python Scripting

This library facilitates writing Python scripts to automate building in Minecraft.  Note that this does not work with realms or console based versions of Minecraft as they do not have the appropriate functionality.  Minecraft has a command to connect to a local server using a websocket connection.  To facilitate iterative development of build scripts, this library consists of a server remains connected to your Minecraft application and a library of commands to send to the server.  The server then relays the commands to the Minecraft application.

To use this library.

1. Start the server using the following command.  The server will print out a command that you should run within the Minecraft chat window.
python -m wsminer.server

2. Startup Minecraft

3. Connect to the server using the command that was printed out by the server.  This should be run from the chat window.

4. Write and run a Python script to connect to the server and send commands.

``` PYTHON
import asyncio
import wsminer

async def main():
    client = wsminer.Client()
    await client.connect()
    await client.build_pyramid(20, 'glowstone')
    # await client.draw_cone(50, 'ice')
    # await client.draw_sphere(20, 'cobblestone')
    # await client.draw_image_nn("butterfly.png")

asyncio.get_event_loop().run_until_complete(main())

```
