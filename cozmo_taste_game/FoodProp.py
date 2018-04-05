from abc import ABC, abstractmethod

# Constants of the taste types so a small typo doesn't cause
# Use these and not raw strings
sour = "sour"
salty = "salty"
bitter = "bitter"
umami = "umami"
savory = umami
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



class Hotdog(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "hotdog"

    @property
    def tastes(self):
        return [savory]

class Watermelon(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "watermelon"

    @property
    def tastes(self):
        return [sweet]

class Saltshaker(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "salt"

    @property
    def tastes(self):
        return [salty]

class Broccoli(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "broccoli"

    @property
    def tastes(self):
        return [bitter]

class Lemon(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "lemon"

    @property
    def tastes(self):
        return [sour]


def get_food(food_type: str):
    """
    Factory function

    :param food_type: String representing what food to return
    :return: Reference to the suitable static food object
    :exception: KeyError if food_type isn't in dictionary
    """
    food_type = food_type.lower()
    return {
        "hotdog": Hotdog(),
        "watermelon": Watermelon(),
        "broccoli": Broccoli(),
        "saltshaker": Saltshaker(),
        "lemon": Lemon()
    }[food_type]
