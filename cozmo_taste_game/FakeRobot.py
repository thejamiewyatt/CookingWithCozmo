
class FakeRobot():

    def __init__(self):
        pass

    def set_head_angle(*a):
        print("Changed head angle")
        return FakeAction()

    def set_lift_height(*a):
        print("Changed lift height")
        return FakeAction()

    def say_text(*a):
        print("Cozmo says: " + a[1])
        return FakeAction()

    def add_event_handler(*a):
        return FakeAction()

    def turn_in_place(*a):
        print("Turned in place")
        return FakeAction()

    def play_anim_trigger(*a):
        print(f"Played animation {a[1][0]}")
        return FakeAction()

class FakeAction():
    def __init__(self):
        pass

    def wait_for_completed(self):
        pass