import cozmo
from cozmo.util import degrees
import os
import shutil
import requests

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
foodAnalyzer = ResponseAnalyzer.ResponseAnalyzer()



def on_new_camera_image(evt, **kwargs):
    global cameraLock
    global foodAnalyzer
    if(foodAnalyzer.hasBeenChecked and cameraLock.acquire(False)):
        pilImage = kwargs['image'].raw_image
        photo_location = f"photos/fromcozmo-{kwargs['image'].image_number}.jpeg"
        print(f"photo_location is {photo_location}")
        pilImage.save(photo_location, "JPEG")

        with open(photo_location, 'rb') as f:
            # TODO: automate model mounting
            response = requests.post('https://www.floydlabs.com/expose/KZpEfCeWw4U8w5tsiN4PxS', files={'file': f})
            print(response)
            foodAnalyzer.analyzeResponse(response.json())
        
        cameraLock.release()
 
def cozmo_program(robot: cozmo.robot.Robot):
    global cameraLock
    global foodAnalyzer
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

    robot.add_event_handler(cozmo.world.EvtNewCameraImage, on_new_camera_image)

    # Main loop
    while not discoveredObject:

        # Check to see if critical section is open
        if(foodAnalyzer.hasBeenChecked == False and cameraLock.acquire(False) == True):
            print(f'{foodAnalyzer.streakFood}')
            if(foodAnalyzer.hasFoundFood()):
                food = get_food(foodAnalyzer.getFoundFood())
                taster.taste_food(food)
            else:
                amount = -5 if r.getrandbits(1)==0 else 5
                print(amount)
                robot.turn_in_place(degrees(amount)).wait_for_completed()
                
            cameraLock.release() 
            #time.sleep(1)
        else:
            pass # Picture currently being taken or processing



cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
