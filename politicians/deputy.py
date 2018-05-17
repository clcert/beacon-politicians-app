import json
import os
from updater import Updater


class Deputy:
    def __init__(self):
        self.json_path = os.path.dirname(os.path.realpath(__file__)) + '/static/json/deputies.json'
        self.info = self.get_info()

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

    def get_info(self):
        """
        Get deputy's information if the file is json formatted, else
        update the file and return the information.
        :return:
        """
        if self.check_format():
            with open(self.json_path, 'r') as infile:
                json_file = json.load(infile)

                return json_file

        else:
            u = Updater()
            u.update(u.get_index())
            return self.get_info()
