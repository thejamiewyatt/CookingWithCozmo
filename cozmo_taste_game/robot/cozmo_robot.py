from .robot import Robot
from cozmo.util import degrees
from cozmo.world import EvtNewCameraImage
from random import randint, getrandbits
from cozmo.anim import Triggers


class CozmoRobot(Robot):
    """Wrapper class for a :class:`cozmo.robot.Robot`"""

    def __init__(self, cozmo):
        self.cozmo = cozmo
        self.current_angle = 0

    def add_event_handler(self, on_new_camera_image) -> None:
        self.cozmo.add_event_handler(EvtNewCameraImage, on_new_camera_image)

    def set_start_position(self) -> None:
        """Sets the start position.

        :return: None
        """
        self.cozmo.set_head_angle(degrees(0)).wait_for_completed()
        self.cozmo.set_lift_height(0.0).wait_for_completed()

    def speak(self, text: str) -> None:
        """Wrapper method for :meth:`~cozmo.robot.Robot.say_text`.

        :param text: The text to say
        :return: None
        """
        self.cozmo.say_text(str(text)).wait_for_completed()

    def turn_in_place(self) -> None:
        """Wrapper method for :meth:`~cozmo.robot.Robot.turn_in_place`.

        :return: None
        """
        rotation_amount = self.__get_rotation_amount()
        self.current_angle += rotation_amount
        self.cozmo.turn_in_place(degrees(rotation_amount)).wait_for_completed()

    def __get_rotation_amount(self) -> int:
        """Gets an amount to rotate.

        :return: The amount to rotate
        """
        min_rotate_angle = -10
        max_rotate_angle = 10

        if self.current_angle <= min_rotate_angle:
            rotation_amount = 5 + randint(0, 7)

        elif self.current_angle >= max_rotate_angle:
            rotation_amount = -5 - randint(0, 7)

        else:
            rotation_amount = 5 if getrandbits(1) == 0 else -5

            if rotation_amount < 0:
                rotation_amount -= randint(0, 7)
            else:
                rotation_amount += randint(0, 7)

        return rotation_amount

    def react_positively(self) -> None:
        """Performs a positive reaction. Chooses a random number
        from 0 to 4 and plays reaction that is tied to that number.

        :return: None
        """
        positive_reactions = [
            Triggers.MajorWin,
            Triggers.CodeLabHappy,
            Triggers.CodeLabYes,
            Triggers.CodeLabAmazed,
            Triggers.CodeLabCelebrate
        ]

        num = randint(0, 4)
        if num == 0:
            self.speak("That is Perfect!")
            self.__play_animation(positive_reactions[num])
        elif num == 1:
            self.__play_animation(positive_reactions[num])
            self.speak("Thank you!")
        elif num == 2:
            self.__play_animation(Triggers.CodeLabCurious)
            self.__play_animation(positive_reactions[num])
        elif num == 3:
            self.__play_animation(positive_reactions[num])
        else:
            self.speak("Yes, you got it!")
            self.__play_animation(positive_reactions[num])

    def react_negatively(self) -> None:
        """Performs a negative reaction. Chooses a random number
        from 0 to 4 and plays reaction that is tied to that number.

        :return: None
        """

        negative_reactions = [
            Triggers.MajorFail,
            Triggers.CubeMovedUpset,
            Triggers.CodeLabUnhappy,
            Triggers.PounceFail,
            Triggers.CodeLabBored
        ]
        num = randint(0, 4)
        if num == 0:
            self.__play_animation(negative_reactions[num])
            self.speak("I don't need that")
        elif num == 1:
            self.__play_animation(negative_reactions[num])
            self.speak("Try again please.")
        elif num == 2:
            self.__play_animation(Triggers.CodeLabCurious)
            self.speak("No")
            self.__play_animation(negative_reactions[num])
        elif num == 3:
            self.speak("That's not what we need.")
            self.__play_animation(negative_reactions[num])
        else:
            self.__play_animation(negative_reactions[num])
            
    def check_plate_and_celebrate(self, distance, speed, deg) -> None:
        """
        :param distance: distance to drive in mm
        :param speed: speed that cozmo will drive
        :param deg: degrees cozmo will turn
        :return: None
        """
        #
        self.speak("Hooray, we made my favorite foods! Bye Bye!")
        self.cozmo.turn_in_place(degrees(deg)).wait_for_completed()
        # self.cozmo.drive_straight(distance_mm(distance), speed_mmps(speed)).wait_for_completed()
        self.cozmo.play_anim_trigger(Triggers.PopAWheelieInitial, ignore_body_track=True).wait_for_completed()
        self.cozmo.play_anim_trigger(Triggers.FeedingAteFullEnough_Normal).wait_for_completed()
        self.cozmo.play_anim_trigger(Triggers.DriveEndHappy).wait_for_completed()

    def __play_animation(self, anim_trigger) -> None:
        """Wrapper method for :meth:`~cozmo.robot.Robot.play_anim_trigger`.

        :param anim_trigger: The animation to perform
        :return: None
        """
        self.cozmo.play_anim_trigger(anim_trigger, ignore_body_track=True).wait_for_completed()


