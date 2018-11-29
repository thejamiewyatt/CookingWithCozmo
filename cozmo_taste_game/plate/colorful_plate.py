from .plate import Plate
from cozmo_taste_game import FoodProp
from typing import List


class ColorfulPlate(Plate):
    """Colorful plate class: the goal is to fill the plate with recipe items."""
    def __init__(self):
        super().__init__()
        #self.goal_num_colors = 3

    def add_food(self, food: FoodProp, recipe) -> None:
        """Adds a food to the plate

        :param food: A food prop object to add to the plate
        :return: None
        """
        if not self.can_place_food(food, recipe):
            raise Exception('Cannot place a food with that color on the colorful plate')

        self.foods.append(food)

    def can_place_food(self, food_to_be_placed: FoodProp, recipe) -> bool:
        """Determines whether or not food can be placed on the plate.

        :param food_to_be_placed: The food prop object to be placed on the plate
        :return: bool
        """
        print(recipe)
        if food_to_be_placed.name in recipe:
            return True
        else:
            return False

    @property
    def names(self) -> List[str]:
        """The name currently on the plate.
        :return: The name currently on the plate.
        """

        return [food.name for food in self.foods] 

    @property
    def is_full(self) -> bool:
        """The plate is full if there is a certain number of colors.
        :return: bool
        """
        if self.goal_num_colors == len(self.colors):
            return True
        else:
            return False

