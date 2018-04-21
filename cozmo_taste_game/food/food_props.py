from .food_prop import FoodProp
from .food_group import FoodGroup


class Hotdog(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'hotdog'

    @property
    def food_groups(self):
        return [FoodGroup.protein]

    @property
    def color(self):
        return 'red'


class Watermelon(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'watermelon'

    @property
    def food_groups(self):
        return [FoodGroup.fruit]

    @property
    def color(self):
        return 'red'


class Saltshaker(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'salt'

    @property
    def food_groups(self):
        return []

    @property
    def color(self):
        return 'white'


class Broccoli(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'broccoli'

    @property
    def food_groups(self):
        return [FoodGroup.vegetable]

    @property
    def color(self):
        return 'green'


class Lemon(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'lemon'

    @property
    def food_groups(self):
        return [FoodGroup.fruit]

    @property
    def color(self):
        return 'yellow'


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
