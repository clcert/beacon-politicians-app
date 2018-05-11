import json
import random


class Deputy:
    def __init__(self):

        # Try to get deputies dictionary
        with open('static/json/deputies.json') as f:
            deputies = json.load(f)
        max_index = len(deputies)

        # TO DO: Change using beacon random generator
        self.index = random.randint(0, max_index-1)

        # dict containing deputy's information
        self.info = deputies[self.index]
