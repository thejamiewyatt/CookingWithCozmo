import cozmo
import random
from FoodProp import *
from PIL import Image

face_image = Image.open("./openEye.png")
# resize to fit on Cozmo's face screen
face_image = face_image.resize(cozmo.oled_face.dimensions(), Image.BICUBIC)
# convert the image to the format used by the oled screen
face_image = cozmo.oled_face.convert_image_to_screen_data(face_image,
                                                              invert_image=True)


def on_new_camera_image(evt, **kwargs):
    global isProcessing
    global isTakingPicture
    global discoveredObject

    if isTakingPicture:
        if not isProcessing:
            if not discoveredObject:
                isProcessing = True
                pilImage = kwargs['image'].raw_image
                photo_location = f"photos/fromcozmo-{kwargs['image'].image_number}.jpeg"
                print(f"photo_location is {photo_location}")
                pilImage.save(photo_location, "JPEG")
                with open(photo_location, 'rb') as f:
                    r = requests.post('https://www.floydlabs.com/expose/HKFD7SppfGmtYDhcGyHsyH', files={'file': f})
                    # r = requests.post('https://www.floydlabs.com/expose/HKFD7SppfGmtYDhcGyHsyH', files={'file', (photo_location, f, 'image/jpeg')})
                    # r = requests.post('https://www.floydlabs.com/expose/HKFD7SppfGmtYDhcGyHsyH')
                parseResponse(r.json())
                isProcessing = False


def react(rank, r):
    """

    :param rank: The rank given to the food to choose reaction
    :param r: The robot to run commands on
    :return: None
    """
    print(rank)
    if rank == 0:
        r.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()
    elif rank == 1:
        r.play_anim_trigger(cozmo.anim.Triggers.CubeMovedUpset).wait_for_completed()
    elif rank == 2:
        r.play_anim_trigger(cozmo.anim.Triggers.NothingToDoBoredIntro).wait_for_completed()
        r.play_anim_trigger(cozmo.anim.Triggers.NeutralFace).wait_for_completed()
    elif rank == 3:
        r.play_anim_trigger(cozmo.anim.Triggers.MajorWin).wait_for_completed()
    else:
        r.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()


def det_fav_taste():
    """
    This function creates a list of flavors and shuffles them
    :return: shuffled list of flavors
    """
    flavors = ["sweet", "salty", "sour", "savory", "bitter"]
    random.shuffle(flavors)
    return flavors


def rank_food(food, taste):
    for i, taste in enumerate(taste):
        if taste in food.getTasteTypes():
            rank = i
    return rank


def cozmo_program(robot: cozmo.robot.Robot):
    flavors = det_fav_taste()
    apple = Apple()
    rank = rank_food(apple, flavors)
    react(rank, robot)
    ##


cozmo.run_program(cozmo_program)

"""
import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps
import sys
import os
import shutil
import requests
import json
import time
import asyncio
import datetime

isProcessing = False
isTakingPicture = False
targetObject = 'seltzer'
discoveredObject = False


def parseResponse(response):
    print(f"response is {response}")
    global targetObject
    global discoveredObject
    entries = {}
    highestConfidence = 0.0
    highestEntry = ''
    print(response)
    for key in response.keys():
        if key == "answer":
            for guess in response[key].keys():
                print(f"guess: {guess}")
                entries[response[key][guess]] = guess
    for key in entries.keys():
        if key > highestConfidence:
            highestConfidence = key
            highestEntry = entries[key]
    if highestConfidence > 0.8:
        if targetObject == highestEntry:
            discoveredObject = True



def cozmo_program(robot: cozmo.robot.Robot):
    global isTakingPicture
    global targetObject
    targetObject = sys.argv[1]
    if os.path.exists('photos'):
        shutil.rmtree('photos')
    if not os.path.exists('photos'):
        os.makedirs('photos')

    robot.say_text(f"Somebody lost the {targetObject}. Don't worry, I'll find it.").wait_for_completed()
    
    # reset Cozmo's arms and head
    robot.set_head_angle(degrees(10.0)).wait_for_completed()
    robot.set_lift_height(0.0).wait_for_completed()

    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)

    while not discoveredObject:
        isTakingPicture = False
        robot.turn_in_place(degrees(45)).wait_for_completed()
        isTakingPicture = True
        time.sleep(2)

    isTakingPicture = False

    if discoveredObject:
        robot.drive_straight(distance_mm(200), speed_mmps(300)).wait_for_completed()
        robot.say_text(f"Oh yay! I've found the {targetObject}").wait_for_completed()
        robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin).wait_for_completed()

cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
"""