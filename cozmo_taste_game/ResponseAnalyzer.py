# Class responsible for analyzing the json returned from the server
# At the moment, getFoundFood() will only return a valid value if the same
# Prop has been seen 3 times in a row with a confidence > .7

class ResponseAnalyzer():

    def __init__(self):
        self.streak = 0
        self.streakFood = None
        self.identifiedFood = None
        self.hasBeenChecked = True
        
    # input: response json
    def analyzeResponse(self, response):
        self.hasBeenChecked = False
        highestConfidence = 0.0
        highestEntry = ''

        entries = {}
        
        for key in response.keys():
            if key == "answer":
                for guess in response[key].keys():
                    print(f"guess: {guess}")
                    entries[response[key][guess]] = guess
        for key in entries.keys():
            print(f'{entries[key]}: {key}')
            if key > highestConfidence:
                highestConfidence = key
                highestEntry = entries[key]

        
        if highestConfidence > 0.7:
            if(highestEntry == self.streakFood):
                self.streak += 1
                if(self.streak >= 3):
                    self.identifiedFood = self.streakFood
                    self.streak = 0
            else:
                self.streakFood = highestEntry
                self.streak = 0

    def getFoundFood(self):
        self.hasbeenChecked = True
        if(self.identifiedFood != None):
            food = self.identifiedFood
            self.identifiedFood = None
            return food
        else:
            # Occurs when no valid food has been identified
            raise Exception("")

    def hasFoundFood(self):
        self.hasBeenChecked = True
        if(self.identifiedFood != None):
            return True
        else:
            return False


