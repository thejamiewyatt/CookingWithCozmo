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


class Grapes(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'grapes'

    @property
    def color(self):
        return 'green'


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


class Milk(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'milk'

    @property
    def color(self):
        return 'white'


class Banana(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'banana'

    @property
    def color(self):
        return 'yellow'


class Blueberry(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'blueberry'

    @property
    def color(self):
        return 'blue'


class Cupcake(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'cupcake'

    @property
    def color(self):
        return 'pink'


class Cheese(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'cheese'

    @property
    def color(self):
        return 'yellow'


class Carrot(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'carrot'

    @property
    def color(self):
        return 'orange'


class Orange(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'orange'

    @property
    def color(self):
        return 'orange'


class Corn(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'corn'

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
        "grapes": Grapes(),
        "blueberry": Blueberry(),
        "cupcake": Cupcake(),
        "banana": Banana(),
        "carrot": Carrot(),
        "cheese": Cheese(),
        "milk": Milk(),
        "orange": Orange(),
        "corn": Corn()
    }[food_type]
