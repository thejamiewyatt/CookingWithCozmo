import threading
import cozmo
import os
import shutil
from sys import argv
from time import sleep
from random import choice

from cozmo_taste_game import FakeRobot, CozmoRobot
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


def cozmo_program(robot=None):
    global food_analyzer
    global camera_lock
    global photo_location
    photo_location = None

    if DEBUG_MODE:
        robot = FakeRobot()
    else:
        robot = CozmoRobot(robot)

    foods = ['hotdog', 'milk', 'blueberry', 'broccoli', 'cupcake', 'carrot']

    create_photo_directory()
    plate = ColorfulPlate()
    robot.add_event_handler(on_new_camera_image)
    robot.speak('I''m hungry')
    robot.set_start_position()

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
                    if not plate.is_full:
                        robot.speak("Please add another food to the plate")

                else:
                    robot.speak('There is already a {} food on the plate'.format(food.color))
                    robot.react_negatively()

                robot.set_start_position()

                print('{}\n'.format(plate))

            else:
                pass

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


if DEBUG_MODE:
    cozmo_program()
else:
    cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
