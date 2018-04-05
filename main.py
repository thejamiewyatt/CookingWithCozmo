import cozmo
from cozmo.util import degrees
import os
import shutil
import requests
from sys import argv, exit

import threading
import random as r
from cozmo_taste_game import get_food
from cozmo_taste_game import Taster
from cozmo_taste_game import FoodProp

from cozmo_taste_game import ResponseAnalyzer

r.seed()
discoveredObject = False
cameraLock = threading.Lock()
latestPicture = None
foodAnalyzer = ResponseAnalyzer.ResponseAnalyzer(.65, 2)
endpointURL = None
MIN_ROTATE_ANGLE = -10
MAX_ROTATE_ANGLE = 10
currentAngle = 0

if(len(argv) != 2):
    print("Error: please supply endpoint url")
    exit(-1)
else:
    endpointURL = argv[1]
    #r = requests.get(endpointURL)
    #if(r.status_code != 200 or r.status_code != 405):
    #    raise requests.exceptions.HTTPError(f'{endpointURL} is not available')
    #

def on_new_camera_image(evt, **kwargs):
    global cameraLock
    global foodAnalyzer
    global endpointURL
    if(foodAnalyzer.hasBeenChecked and cameraLock.acquire(False)):
        pilImage = kwargs['image'].raw_image
        photo_location = f"photos/fromcozmo-{kwargs['image'].image_number}.jpeg"
        print(f"photo_location is {photo_location}")
        pilImage.save(photo_location, "JPEG")

        with open(photo_location, 'rb') as f:
            # TODO: automate model mounting
            response = requests.post(endpointURL, files={'file': f})
            if response.status_code == 200:
                foodAnalyzer.analyzeResponse(response.json())
        
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

        # Check to see if critical section is open
        if(foodAnalyzer.hasBeenChecked == False and cameraLock.acquire(False) == True):
            print(f'{foodAnalyzer.streakFood}')
            if(foodAnalyzer.hasFoundFood()):
                food = get_food(foodAnalyzer.getFoundFood())
                robot.say_text(str(food)).wait_for_completed()
                rank = taster.taste_food(food)
            else:

                if(currentAngle <= MIN_ROTATE_ANGLE):
                    rotationAmount = 5 + r.randint(0,7)
                elif(currentAngle >= MAX_ROTATE_ANGLE):
                    rotationAmount = -5 - r.randint(0,7)
                else:
                    rotationAmount = 5 if r.getrandbits(1) == 0 else -5
                    if(rotationAmount < 0):
                        rotationAmount -= r.randint(0,7)
                    else:
                        rotationAmount += r.randint(0,7)

                currentAngle += rotationAmount
                robot.turn_in_place(degrees(rotationAmount)).wait_for_completed()

            cameraLock.release() 

        else:
            pass # Picture currently being taken or processing



cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
