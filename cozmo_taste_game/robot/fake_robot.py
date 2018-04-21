from .robot import Robot


class FakeRobot(Robot):
    """Fake robot used for development and testing."""
    def __init__(self):
        pass

    def set_start_position(self) -> None:
        print('Cozmo get setup in a starting position')

    def turn_in_place(self) -> None:
        print('Cozmo turns in place')

    def speak(self, text) -> None:
        print('Cozmo says: {}'.format(text))

    def react_positively(self) -> None:
        print('Cozmo reacts positively')

    def react_negatively(self) -> None:
        print('Cozmo reacts negatively')
