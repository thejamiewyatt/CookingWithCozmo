from .plate import Plate
from cozmo_taste_game import FoodProp
from typing import List


class ColorfulPlate(Plate):
    def __init__(self):
        super().__init__()
        self.goal_colors = ['red', 'orange', 'yellow', 'green', 'blue']
        self.goal_num_food = len(self.goal_colors)

    def add_food(self, food: FoodProp) -> None:
        if not self.can_place_food(food):
            raise Exception('Cannot place a food with that color on the colorful plate')

        self.foods.append(food)

    def can_place_food(self, food_to_be_placed: FoodProp) -> bool:
        if food_to_be_placed.color not in self.colors:
            return True
        else:
            return False

    @property
    def colors(self) -> List[str]:
        return [food.color for food in self.foods]

    @property
    def is_full(self):
        for goal_color in self.goal_colors:
            if goal_color not in self.colors:
                return False
        return True

