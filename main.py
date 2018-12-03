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

    foods = ['milk', 'strawberry', 'blueberries', 'apple', 'egg', 'cheese', 'pepper', 'flour', 'crust', 'cheese', 'tomato', 'chocolate']

    smoothie = ['blueberries', 'strawberry', 'milk']
    fruitSalad = ['apple', 'strawberry', 'blueberries']
    omelete = ['egg', 'cheese', 'pepper']
    pie = ['flour', 'egg', 'apple']
    pizza = ['crust', 'tomato', 'cheese']
    chocolateCake = ['chocolate', 'flour', 'egg']
    recipeString =  ['smoothie', 'fruitSalad', 'omelete', 'pie', 'pizza', 'chocolateCake']
    recipes = [smoothie, fruitSalad, omelete, pie, pizza, chocolateCake]

    create_photo_directory()
    plate = ColorfulPlate()
    robot.add_event_handler(on_new_camera_image)
    robot.speak('I''m hungry')
    robot.set_start_position()

    counter = -1
    for recipe in recipes:
        foodsFound = []

        counter += 1
        allFoodsFound = False

        robot.speak("Lets make a " + recipeString[counter])
        robot.speak("We will need " + recipe[0] +  ", " + recipe[1] + ", and " + recipe[2]) 
        sleep(2)
        while not allFoodsFound: 


            #robot.speak("We need another item")            
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
                   
                    if plate.can_place_food(food, recipe):
                        robot.react_positively()
                        plate.add_food(food, recipe)
                        foodsFound.append(food.name)
                        recipe.remove(food.name)
                        if len(recipe) == 0:
                            allFoodsFound = True
                        #if allFoodsFound == False:
			    #Add another food to the plate	
                    else:
                        if(food.name == "empty"):
                            robot.speak("Please add a food to the plate")
                        elif(food.name in foodsFound):
                            robot.speak('{} has already been added, try again'.format(food.name))
                        else:
                            robot.speak('{} is not part of this recipe, try again'.format(food.name))
                        robot.react_negatively()

                    robot.set_start_position()

                    print('{}\n'.format(plate))
                    if(len(recipe)==3):
                        robot.speak("We still need " + recipe[0] +  ", " + recipe[1] + ", and " + recipe[2])
                    elif(len(recipe)==2):
                        robot.speak("We still need " + recipe[0] + " and " + recipe[1])
                    elif(len(recipe)==1):
                        robot.speak("We still need " + recipe[0])

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


