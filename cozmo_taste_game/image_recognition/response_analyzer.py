"""Class responsible for analyzing the pictures Cozmo takes.
At the moment, getFoundFood() will only return a valid value if the same
Prop has been seen (streak_threshold) times in a row with a confidence > (threshold)
"""
from .tensor_functions import analyze_photo


class ResponseAnalyzer:



    def __init__(self, threshold, streak_threshold, isDebugMode):

        """
        Construct a response analyzer
        :param threshold: Confidence threshold for determining if Cozmo has seen an object or not
        :param streak_threshold: How many times in a row the confidence has to be higher than the threshold
        :param isDebugMode: Is debugging mode on (Currently unused)
        :return: A string of what Cozmo has seen
        """

        self.streak = 0
        self.streakFood = None
        self.identified_food = None
        self.has_been_checked = True
        self.threshold = threshold
        self.streak_threshold = streak_threshold
        self.DEBUG_MODE = isDebugMode

    # input: response json
    def analyze_response(self, file_name):

        """
        Analyze a photo at location file_name. You feed this function pictures, it analyzes them with
        the tensorflow model. Once it analyzes the picture, it sees if it has seen the same object more than
        (streak_threshold) times. If it has, it sets identified_food to what it has found.

        Upon entering the function, the has_been_checked flag gets flipped to False.

        :param file_name: location of a jpg file Cozmo has taken
        :return: None
        """

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
        """
         Get what the response analyzer has decided Cozmo has seen
         Note: Only call this if you are sure cozmo has found something.
         Use has_found_food() before calling this function

         :return: A string of what Cozmo has seen
         """

        self.has_been_checked = True
        if self.identified_food is not None:
            food = self.identified_food
            self.identified_food = None
            return food
        else:
            pass
            # Occurs when no valid food has been identified
            #raise Exception("")

    def force_input(self, foodItem):
        """
         Force the response analyzer to see a food item

         :param foodItem: a string of what cozmo should see
         :return: None
         """

        self.identified_food = foodItem
        self.has_been_checked = False

    def has_found_food(self):
        """
         Check if Cozmo has found food. Call this before calling get_found_food()

         :return: True if Cozmo has found something, False otherwise
         """

        self.has_been_checked = True
        if self.identified_food is not None:
            #print("boy")
            return True
        else:
            #print("girl")
            return False
