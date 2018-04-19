import traceback

import cozmo
from cozmo.util import degrees
import os
import shutil
import requests
from sys import argv, exit

import threading
import random as r

from cozmo_taste_game import FakeRobot
from cozmo_taste_game import get_food
from cozmo_taste_game import Taster
from cozmo_taste_game import FoodProp

from cozmo_taste_game import ResponseAnalyzer

r.seed()
discoveredObject = False
cameraLock = threading.Lock()
latestPicture = None

endpointURL = None
MIN_ROTATE_ANGLE = -10
MAX_ROTATE_ANGLE = 10
currentAngle = 0
DEBUG_MODE = False

if len(argv) != 2:
    print("Error: please supply endpoint url")
    exit(-1)
else:
    if(argv[1] == "-g"):
        DEBUG_MODE = True
    else:
        endpointURL = argv[1]
    # r = requests.get(endpointURL)
    # if(r.status_code != 200 or r.status_code != 405):
    #    raise requests.exceptions.HTTPError(f'{endpointURL} is not available')
    #

foodAnalyzer = ResponseAnalyzer.ResponseAnalyzer(.65, 2, DEBUG_MODE)

def on_new_camera_image(evt, **kwargs):
    global cameraLock
    global foodAnalyzer
    global endpointURL
    if foodAnalyzer.has_been_checked and cameraLock.acquire(False):
        pil_image = kwargs['image'].raw_image
        photo_location = f"photos/fromcozmo-{kwargs['image'].image_number}.jpeg"
        print(f"photo_location is {photo_location}")
        pil_image.save(photo_location, "JPEG")

        with open(photo_location, 'rb') as f:
            # TODO: automate model mounting
            response = requests.post(endpointURL, files={'file': f})
            if response.status_code == 200:
                foodAnalyzer.analyze_response(response.json())

        cameraLock.release()


def cozmo_program(robot: cozmo.robot.Robot):
    global cameraLock
    global foodAnalyzer
    global currentAngle

    taster = Taster(robot)
    taster.get_new_preferences()

    # Where photos will be stored during runtime
    if os.path.exists('photos'):
        shutil.rmtree('photos')
    if not os.path.exists('photos'):
        os.makedirs('photos')

    # reset Cozmo's arms and head
    robot.set_head_angle(degrees(10.0)).wait_for_completed()
    robot.set_lift_height(0.0).wait_for_completed()

    robot.say_text("I'm hungry").wait_for_completed()
    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)

    # Main loop
    while True:

        if DEBUG_MODE:
            foodAnalyzer.force_input(input("Enter food cozmo sees: "))
        # Check to see if critical section is open
        if foodAnalyzer.has_been_checked == False and (DEBUG_MODE or cameraLock.acquire(False) == True):
            # print(f'{foodAnalyzer.streakFood}')
            if foodAnalyzer.has_found_food():
                food = get_food(foodAnalyzer.getFoundFood())
                robot.say_text(str(food)).wait_for_completed()
                rank = taster.taste_food(food)
            else:

                if currentAngle <= MIN_ROTATE_ANGLE:
                    rotation_amount = 5 + r.randint(0, 7)
                elif currentAngle >= MAX_ROTATE_ANGLE:
                    rotation_amount = -5 - r.randint(0, 7)
                else:
                    rotation_amount = 5 if r.getrandbits(1) == 0 else -5
                    if rotation_amount < 0:
                        rotation_amount -= r.randint(0, 7)
                    else:
                        rotation_amount += r.randint(0, 7)

                currentAngle += rotation_amount
                robot.turn_in_place(degrees(rotation_amount)).wait_for_completed()
            if not DEBUG_MODE:
                cameraLock.release()

        else:
            pass  # Picture currently being taken or processing

if not DEBUG_MODE:
    cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
else:
    try:
        cozmo_program(FakeRobot.FakeRobot())
    except AttributeError as ae:

        print(traceback.format_exc())
        if(str(ae)[1:10] == "FakeRobot"):
            print(f"\nThe function '{str(ae)[-5:-1]}' hasn't been added to the dummy class")
            print("or you're trying to reference a variable that doesn't exist")
            print(f"Add the following lines to cozmo_taste_game/FakeRobot.py:")
            print(f"def {str(ae)[-5:-1]}(a*):")
            print(f"\tprint('#Give helpful input here#')")
            print(f"\treturn FakeAction()")

