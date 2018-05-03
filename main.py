import threading
import traceback
import cozmo
import os
import shutil
from sys import argv, exit
from time import sleep
from random import choice

from cozmo_taste_game import Robot, FakeRobot, CozmoRobot
from cozmo_taste_game import ColorfulPlate, get_food
from cozmo_taste_game import ResponseAnalyzer

# Globals
DEBUG_MODE = False
camera_lock = threading.Lock()
food_analyzer = ResponseAnalyzer(.65, 2, DEBUG_MODE)
discovered_object = False
latest_picture = None

if len(argv) > 1:
    if argv[1] == "-g":
        DEBUG_MODE = True



def cozmo_program(robot):
    global food_analyzer
    global camera_lock
    global photo_location
    photo_location = None

    robot = CozmoRobot(robot)

    foods = ['hotdog', 'lemon', 'saltshaker', 'broccoli', 'watermelon']

    create_photo_directory()
    plate = ColorfulPlate()
    robot.add_event_handler(on_new_camera_image)
    #robot.speak('I''m hungry')
    #robot.set_start_position()

    while not plate.is_full:

        if DEBUG_MODE:
            input('Press enter to have Cozmo find a food')
            random_food = choice(foods)
            food_analyzer.force_input(random_food)

        # Check to see if critical section is open
        if photo_location is not None:
            food_analyzer.analyze_response(photo_location)
            photo_location = None

        if not food_analyzer.has_been_checked and (DEBUG_MODE or camera_lock.acquire(False)):

            if food_analyzer.has_found_food():
                # Cozmo found a food
                food_string = food_analyzer.get_found_food()
                food = get_food(food_string)

                robot.speak(str(food))

                if plate.can_place_food(food):
                    robot.react_positively()
                    plate.add_food(food)
                else:
                    print('cannot place the food')
                    robot.react_negatively()

                print(plate)
                print()

            else:
                pass
                #robot.turn_in_place()

            if not DEBUG_MODE:
                camera_lock.release()

        else:
            pass  # Picture currently being taken or processing
    
    robot.check_plate_and_celebrate(0, 10, -130)
    

def on_new_camera_image(evt, **kwargs):
    global food_analyzer
    global camera_lock
    global photo_location

    if photo_location is None and food_analyzer.has_been_checked and camera_lock.acquire(False):
        sleep(1)
        pil_image = kwargs['image'].raw_image
        photo_location = f"photos/fromcozmo-{kwargs['image'].image_number}.jpeg"
        print(f"photo_location is {photo_location}")
        pil_image.save(photo_location, "JPEG")

        camera_lock.release()


def create_photo_directory():
    if os.path.exists('photos'):
        shutil.rmtree('photos')
    if not os.path.exists('photos'):
        os.makedirs('photos')


if not DEBUG_MODE:
    #cozmo.run_program(CozmoRobot(cozmo_program, on_new_camera_image), use_viewer=True, force_viewer_on_top=True)
    cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)

else:
    try:
        cozmo_program(FakeRobot())
    except AttributeError as ae:

        print(traceback.format_exc())
        if str(ae)[1:10] == "FakeRobot":
            print(f"\nThe function '{str(ae)[-5:-1]}' hasn't been added to the dummy class")
            print("or you're trying to reference a variable that doesn't exist")
            print(f"Add the following lines to cozmo_taste_game/fake_robot.py:")
            print(f"def {str(ae)[-5:-1]}(a*):")
            print(f"\tprint('#Give helpful input here#')")
            print(f"\treturn FakeAction()")
