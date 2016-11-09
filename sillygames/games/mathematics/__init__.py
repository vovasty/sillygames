#!/usr/bin/env python3

import sys
import time
import cozmo
import random
import math
import sillygames
import os
import asyncio

from PIL import Image, ImageDraw, ImageFont

def calc(a, sign, b):
    if sign == "+":
        return a + b
    if sign == "-":
        return a - b
    if sign == "*":
        return a * b
    if sign == "/":
        return math.floor(a / b)

def generateImage(text, font=os.path.join(os.path.dirname(__file__), "font.ttf"), fontSize=100, imageSize=(300, 100)):
    image = Image.new('RGBA', imageSize, (255, 255, 255, 255))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font, fontSize)
    
    width, height = draw.textsize(text, font=font)
    
    draw.text(((imageSize[0] - width)/2, (imageSize[1] - height)/2), text, (0,0,0), font=font)
    return image

def randomEquation(max_multiply = 10, max_add = 100):
    sign = random.choice('+-/*')
    if sign == "+":
        a = random.randrange(1, max_add / 2)
        b = random.randrange(1, 10)
    if sign == "-":
        a = random.randrange(1, max_add)
        b = random.randrange(1, min(a, 10))
    elif sign == "*":
        a = random.randrange(1, max_multiply / 2)
        b = random.randrange(1, math.floor(max_multiply / a))
    elif sign == "/":
        a = random.randrange(1, max_multiply)
        d = random.randrange(1, math.floor(a / 2) + 2)
        b = math.floor(a / d)
        a = b * d

    text = "%s%s%s" % (a, sign, b)
    answer = calc(a, sign, b)
    return (text, answer)

async def main(robot, commander, phrase):
    # move head and lift to make it easy to see Cozmo's face
    await robot.set_lift_height(0.0).wait_for_completed()
    await robot.set_head_angle(cozmo.robot.MAX_HEAD_ANGLE).wait_for_completed()
    
    text, myAnswer = randomEquation()
    myAnswer = str(myAnswer)
    image = generateImage(text, imageSize=cozmo.oled_face.dimensions(), fontSize=25)

    duration_s = 30
    face_image = cozmo.oled_face.convert_image_to_screen_data(image, invert_image=True)
    await robot.say_text(text).wait_for_completed()
    while 1:
        robot.display_oled_face_image(face_image, duration_s * 1000.0)
        yourAnswer = await commander.get()
        
        if yourAnswer == None:
            continue

        if yourAnswer == myAnswer:
            await robot.say_text("Correct!", play_excited_animation=True).wait_for_completed()
        else:
            await robot.say_text(yourAnswer + " is not right!").wait_for_completed()
        
        return

def info():
    return {"activation": "play numbers", "name": "Math", "description": "Basic arithmetic"}
