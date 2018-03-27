import cozmo
from random import shuffle


class Taster:
    def __init__(self, robot):
        """
        Initializes a Taster
        :param robot: A Cozmo instance
        """
        self.robot = robot
        self.tastes = ["sweet", "salty", "sour", "savory", "bitter"]

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

        if rank == 0:
            self.robot.play_anim_trigger(cozmo.anim.Triggers.MajorFail).wait_for_completed()

        elif rank == 1:
            self.robot.play_anim_trigger(cozmo.anim.Triggers.CubeMovedUpset).wait_for_completed()

        elif rank == 2:
            self.robot.play_anim_trigger(cozmo.anim.Triggers.NothingToDoBoredIntro).wait_for_completed()
            self.robot.play_anim_trigger(cozmo.anim.Triggers.NeutralFace).wait_for_completed()

        elif rank == 3:
            self.robot.play_anim_trigger(cozmo.anim.Triggers.MajorWin).wait_for_completed()

        else:
            self.robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabHappy).wait_for_completed()

    def rank_food(self, food):
        """
        Rank is implicit in the ordering of the self.tastes list.
        If the food tastes like multiple things then we just use the first taste.
        :param food: A Food Prop instance
        :return: A ranking of how much the taster likes the food
        """
        return self.tastes.index(food.tastes[0])
