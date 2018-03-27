import cozmo
from FoodProp import *
from Taster import Taster


def cozmo_program(robot: cozmo.robot.Robot):
    taster = Taster(robot)
    taster.get_new_preferences()
    # This is where Cozmo will try to recognize what food is in front of him
    # For now, we just say he recognized an Apple
    food = getFood("apple")
    taster.taste_food(food)


cozmo.run_program(cozmo_program)
