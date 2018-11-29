from abc import ABC, abstractmethod


class FoodProp(ABC):
    """Abstract Food Prop interface."""
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @property
    def food_groups(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass
