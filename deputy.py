import json
import os
import parser.deputies as pd
from updater import Updater


class Deputy:
    def __init__(self, json_index):
        self.json_path = os.path.dirname(os.path.realpath(__file__)) + '/static/json/deputies.json'
        self.json_index = json_index
        self.info = None
        self.load_info()

    def check_format(self):
        """
        Checks if the file format is correct as a json file
        :return: True if the file is formatted as a json, else False
        """
        with open(self.json_path, 'r') as infile:
            try:
                json.load(infile)  # Try to load the file as json

            except ValueError:
                return False

            finally:
                infile.close()

            return True

    def load_info(self):
        """
        Get deputy's information if the file is json formatted, else
        update the file and return the information.
        :return:
        """
        if self.check_format():
            deputies = Updater().get_list()
            self.info = deputies[self.json_index]

        else:
            u = Updater()
            u.update()
            return self.load_info()
