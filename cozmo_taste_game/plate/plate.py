from abc import ABC, abstractmethod
from cozmo_taste_game import FoodProp


class Plate(ABC):
    """Abstract plate interface."""
    def __init__(self):
        self.foods = []

    def __str__(self):
        out = 'Plate: '
        for food in self.foods:
            out += str(food) + ', '

        # Trim last comma and space
        trim_index = len(out) - 2

        return out[:trim_index]

    @abstractmethod
    def can_place_food(self, food: FoodProp, recipe) -> bool:
        pass

    @abstractmethod
    def add_food(self, food: FoodProp, recipe) -> None:
        pass

    @property
    @abstractmethod
    def is_full(self) -> bool:
        pass
