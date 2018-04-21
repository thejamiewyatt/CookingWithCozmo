from .robot import Robot
from cozmo.util import degrees
from cozmo.world import EvtNewCameraImage
from random import randint, getrandbits


class CozmoRobot(Robot):
    """Wrapper class for a :class:`~cozmo.objects.LightCube`"""
    def __init__(self, cozmo, on_new_camera_image):
        self.cozmo = cozmo
        self.cozmo.add_event_handler(EvtNewCameraImage, on_new_camera_image)
        self.current_angle = 0

    def set_start_position(self) -> None:
        """Sets the start position.

        :return: None
        """
        self.cozmo.set_head_angle(degrees(10.0)).wait_for_completed()
        self.cozmo.set_lift_height(0.0).wait_for_completed()

    def speak(self, text: str) -> None:
        """Wrapper method for :meth:`~cozmo.objects.LightCube.set_lights_off`.

        :param text: The text to say
        :return: None
        """
        self.cozmo.say_text(str(text)).wait_for_completed()

    def turn_in_place(self) -> None:
        rotation_amount = self.__get_rotation_amount()
        self.current_angle += rotation_amount
        self.cozmo.turn_in_place(degrees(rotation_amount)).wait_for_completed()

    def __get_rotation_amount(self) -> int:
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

    def react_positively(self):
        print('Cozmo reacts positively')

    def react_negatively(self):
        print('Cozmo reacts negatively')



