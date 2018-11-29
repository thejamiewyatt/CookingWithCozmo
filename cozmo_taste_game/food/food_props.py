from .food_prop import FoodProp
from .food_group import FoodGroup

class Empty(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'empty'

    @property
    def name(self):
        return 'empty'

class Milk(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'milk'

    @property
    def name(self):
        return 'milk'

class Blueberries(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'blueberries'

    @property
    def name(self):
        return 'blueberries'



class Cheese(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'cheese'

    @property
    def name(self):
        return 'cheese'

class Flour(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'flour'

    @property
    def name(self):
        return 'flour'

class Chocolate(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'chocolate'

    @property
    def name(self):
        return 'chocolate'

class Strawberry(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'strawberry'

    @property
    def name(self):
        return 'strawberry'

class Pepper(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'pepper'

    @property
    def name(self):
        return 'pepper'

class Tomato(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'tomato'

    @property
    def name(self):
        return 'tomato'

class Crust(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'crust'

    @property
    def name(self):
        return 'crust'

class Egg(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'egg'

    @property
    def name(self):
        return 'egg'

class Apple(FoodProp):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'apple'

    @property
    def name(self):
        return 'apple'

def get_food(food_type: str):
    """
    Factory function

    :param food_type: String representing what food to return
    :return: Reference to the suitable static food object
    :exception: KeyError if food_type isn't in dictionary
    """
    food_type = food_type.lower()
    return {
        
        "blueberries": Blueberries(),
        "apple" : Apple(),
        "egg" : Egg(),
        "chocolate" : Chocolate(),
        "crust" : Crust(),
        "strawberry" : Strawberry(),
        "tomato" : Tomato(),
        "flour" : Flour(),
        "pepper" : Pepper(),
        "cheese": Cheese(),
        "milk": Milk(),
        "empty": Empty()
       
    }[food_type]
