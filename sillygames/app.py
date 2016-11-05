import cozmo
import sillygames, sillygames.plugins
import time
import sys
import speech_recognition as sr
import asyncio
import glob, os
import logging
    
available_commands=[]
command_activate = "Google"
logger = logging.getLogger()
running_callback = None

def hear(robot, commands):
    logger.debug("listening...")
    recognized = sillygames.recognize()
    if recognized == None:
        logger.debug("Not recognized")
        return

    print("You said: " + recognized)
    if command_activate in recognized or command_activate.lower() in recognized:
        logger.debug("Action command recognized")
        command_phrase = recognized[len(command_activate):].strip().lower()
        command = commands.get(command_phrase)

        if command == None:
            robot.say_text("What?").wait_for_completed()
            return
        command(robot, command_phrase)
        
    else:
        robot.say_text("You did not say the magic word " + command_activate).wait_for_completed()
        logger.debug("You did not say the magic word " + command_activate)

def run(sdk_conn):
    '''The run method runs once the Cozmo SDK is connected.'''
    robot = sdk_conn.wait_for_robot()
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
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            sillygames.setAudioSourceAndRecognizer(source, r)
            while 1:
                print("say something")
                hear(robot, commands)

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