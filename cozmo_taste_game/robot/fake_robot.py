from .robot import Robot


class FakeRobot(Robot):
    """Fake robot used to simulate a game in the absence of Cozmo"""
    def __init__(self):
        pass

    def set_start_position(self) -> None:
        print('Cozmo get setup in a starting position')

    def add_event_handler(self, on_new_camera_image) -> None:
        print('Adding on new camera image event handler to cozmo')

    def turn_in_place(self) -> None:
        print('Cozmo turns in place')

    def speak(self, text) -> None:
        print('Cozmo says: {}'.format(text))

    def react_positively(self) -> None:
        print('Cozmo reacts positively')

    def react_negatively(self) -> None:
        print('Cozmo reacts negatively')

    def check_plate_and_celebrate(self, distance, speed, deg):
        print('Cozmo checks plate and celebrates')
