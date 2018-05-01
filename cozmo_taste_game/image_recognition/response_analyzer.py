"""Class responsible for analyzing the json returned from the server
At the moment, getFoundFood() will only return a valid value if the same
Prop has been seen 3 times in a row with a confidence > .7
"""
from .tensor_functions import analyze_photo


class ResponseAnalyzer:
    def __init__(self, threshold, streak_threshold, isDebugMode):
        self.streak = 0
        self.streakFood = None
        self.identified_food = None
        self.has_been_checked = True
        self.threshold = threshold
        self.streak_threshold = streak_threshold
        self.DEBUG_MODE = isDebugMode

    # input: response json
    def analyze_response(self, file_name):
        self.has_been_checked = False
        highest_confidence = 0.0
        highest_entry = ''


        response = analyze_photo(file_name)
        print(response)
        for food_name, confidence in response.items():
            if confidence > highest_confidence:
                highest_confidence = confidence
                highest_entry = food_name

        if highest_confidence > self.threshold:
            if highest_entry != 'nothing' and highest_entry == self.streakFood:
                self.streak += 1
                if self.streak >= self.streak_threshold:
                    self.identified_food = self.streakFood
                    self.streak = 0
            else:
                self.streakFood = highest_entry
                self.streak = 0

    def get_found_food(self):
        self.has_been_checked = True
        if self.identified_food is not None:
            food = self.identified_food
            self.identified_food = None
            return food
        else:
            # Occurs when no valid food has been identified
            raise Exception("")

    def force_input(self, foodItem):
        self.identified_food = foodItem
        self.has_been_checked = False

    def has_found_food(self):
        self.has_been_checked = True
        if self.identified_food is not None:
            return True
        else:
            return False
