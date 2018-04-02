from abc import ABC, abstractmethod

# Constants of the taste types so a small typo doesn't cause
# Use these and not raw strings
sour = "sour"
salty = "salty"
bitter = "bitter"
umami = "umami"
savory = "umami"
sweet = "sweet"


class FoodProp:
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def tastes(self):
        """

        :return: List of tastes that could include: "sweet", "sour", "salty", "bitter", "umami"
        """
        pass


class Apple(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "apple"

    @property
    def tastes(self):
        return [sweet]


class Orange(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "orange"

    @property
    def tastes(self):
        return [sweet, sour]


def get_food(food_type: str):
    """
    Factory function
    :param food_type: String representing what food to return
    :return: Reference to the suitable static food object
    Exceptions: KeyError if food_type isn't in dictionary
    """
    food_type = food_type.lower()
    return {
        "apple": Apple(),
        "orange": Orange()
    }[food_type]
