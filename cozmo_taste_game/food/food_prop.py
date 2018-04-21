from abc import ABC, abstractmethod


class FoodProp(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @property
    @abstractmethod
    def food_groups(self):
        pass

    @property
    @abstractmethod
    def color(self):
        pass
