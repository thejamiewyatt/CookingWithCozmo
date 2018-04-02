import cozmo
from cozmo.robot import Robot
from cozmo_taste_game import get_food
from cozmo_taste_game import Taster


def cozmo_program(robot: Robot) -> None:
    taster = Taster(robot)
    taster.get_new_preferences()
    # This is where Cozmo will try to recognize what food is in front of him
    # For now, we just say he recognized an Apple
    food = get_food("apple")
    taster.taste_food(food)


cozmo.run_program(cozmo_program)
