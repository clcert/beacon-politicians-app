import json
import datetime
import os
import parser.deputies as pd
import random


class Updater:
    def __init__(self):
        self.json_path = os.path.dirname(os.path.realpath(__file__)) + '/static/json/deputies.json'

    def get_index(self):
        """
        Get a random number in the range of the deputies list length.
        TO DO: Modify using CLCERT Beacon Random
        :return: An integer in the range of the list described.
        """
        max_index = len(pd.Parser().parse_personalinfo()) - 1
        return random.randint(0, max_index)

    def update(self, index):
        """
        Given an index for the position of the deputy at deputies list, modifies the json
        file using deputy's information.
        :param index:
        :return:
        """
        with open(self.json_path, 'w', encoding='utf-8') as outfile:
            dict_deputy = pd.Parser().get_deputy(index)
            dict_deputy['index'] = index

            modified = datetime.datetime.now()
            modified = str(modified)

            dict_deputy = dict(deputy=dict_deputy, modified=modified)
            json.dump(dict_deputy, outfile, ensure_ascii=False)

            outfile.close()
        return

    def run(self):
        return


if __name__ == '__main__':
    updater = Updater()
    updater.run()
