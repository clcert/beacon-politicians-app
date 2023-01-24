import json
import os
from updater import Updater


class Deputy:
    def __init__(self, index):
        self.json_path = os.path.dirname(os.path.realpath(__file__)) + '/deputies.json'
        self.index = index
        self.info = None
        self.load_info()

    def check_format(self):
        """
        Checks if the file format is correct as a json file
        :return: True if the file is formatted as a json, else False
        """
        if not os.path.exists(self.json_path):
            print(self.json_path + ' does not exist')
            return False

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
            self.info = list(
                filter(
                    lambda deputy: deputy['index'] == self.index,
                    deputies,
                )
            )[0]

        else:
            u = Updater()
            u.update()
            return self.load_info()
