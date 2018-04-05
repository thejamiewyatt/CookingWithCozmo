from cozmo.anim import Triggers
from random import shuffle


class Taster:
    def __init__(self, robot):
        """
        Initializes a Taster

        :param robot: A Cozmo instance
        """
        self.robot = robot
        self.tastes = ["sweet", "salty", "sour", "umami", "bitter"]
        self.reactions = [  # Ranked negative to positive
            Triggers.MajorFail,
            Triggers.CubeMovedUpset,
            Triggers.CodeLabBored,
            Triggers.MajorWin,
            Triggers.CodeLabHappy
        ]

    def get_new_preferences(self):
        """
        Shuffles self.tastes so that the Taster has different taste preferences.
        self.tastes are ordered from LEAST favorite (index 0) to MOST favorite.

        :return: None
        """
        shuffle(self.tastes)

    def taste_food(self, food):
        """
        The robot tastes the food and reacts to it.

        :param robot: A Cozmo instance
        :param food: A Food Prop instance
        :return: None
        """
        rank = self.rank_food(food)
        print('Cozmo ranks a(n) {} as a {}'.format(food, rank))
        animation_trigger = self.reactions[rank]
        self.robot.play_anim_trigger(animation_trigger).wait_for_completed()
        return rank

    def rank_food(self, food):
        """
        Rank is implicit in the ordering of the self.tastes list.
        A rank of 0 means that Cozmo really dislikes the food and 5 means that Cozmo really likes the food.
        If the food tastes like multiple things then we just use the first taste.

        :param food: A Food Prop instance
        :return: A ranking of how much the taster likes the food
        """
        return self.tastes.index(food.tastes[0])
