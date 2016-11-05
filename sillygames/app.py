import cozmo
import sillygames, sillygames.plugins
import time
import sys
import speech_recognition as sr
import asyncio
import glob, os
import logging
import asyncio
    
available_commands=[]
command_activate = "Google"
logger = logging.getLogger()
running_callback = None

async def hear(robot, commands, commander):
    logger.debug("listening...")
    recognized = await commander.get()
    
    command = commands.get(recognized)
    
    if command == None:
        await robot.say_text("What?").wait_for_completed()
        return
    await command(robot, commander, recognized)


async def run(sdk_conn):
    '''The run method runs once the Cozmo SDK is connected.'''
    robot = await sdk_conn.wait_for_robot()
    commands = {}
    global available_commands
    
    plugins = sillygames.plugins.PluginLoader(".", "games")
    plugins.load()
    for plugin in plugins.plugins.values():
        info = plugin.info()
        commands[info["activation"].lower()] = plugin.main
        available_commands.append(info)
    
    if callable(running_callback):
        running_callback()
    try:
        commander = sillygames.SpeechCommandsChannel(command_activate)
        commander.start()
        while 1:
            print("say something")
            await hear(robot, commands, commander)

    except KeyboardInterrupt:
        print("")
        print("Exit requested by user")

def availableCommands():
    global available_commands
    
    return available_commands

def main(callback=None):
    global running_callback
    running_callback = callback
    cozmo.setup_basic_logging()
    cozmo.connect(run)