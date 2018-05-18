import json
import datetime
import os
import parser.deputies as pd
import random
import time
import requests
import urllib3


class Updater:
    def __init__(self):
        self.json_path = os.path.dirname(os.path.realpath(__file__)) + '/static/json/deputies.json'

    def index_from_json(self):
        quote_page = 'https://beacon.clcert.cl/beacon/1.0/pulse/last'

        # TODO: Modify after add certificate to the beacon.
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        page = requests.get(quote_page, verify=False)

        json_page = page.json()
        return json_page['outputValue'], json_page['id']

    def get_index(self):
        """
        Get a random number in the range of the deputies list length.
        TO DO: Modify using CLCERT Beacon Random
        :return: An integer in the range of the list described.
        """
        max_index = len(pd.Parser().parse_personalinfo()) - 1

        index, index_id = self.index_from_json()
        random.seed(index)

        return random.randint(0, max_index), index_id

    def update(self, index, index_id):
        """
        Given an index for the position of the deputy at deputies list, modifies the json
        file using deputy's information.
        :param index:
        :param index_id:
        :return:
        """
        with open(self.json_path, 'w', encoding='utf-8') as outfile:
            dict_deputy = pd.Parser().get_deputy(index)

            dict_deputy['index'] = index
            dict_deputy['index_id'] = "https://beacon.clcert.cl/viewer/advanced?id=" + str(index_id)

            modified = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dict_deputy['modified'] = modified

            json.dump(dict_deputy, outfile, ensure_ascii=False)

            outfile.close()
        return

    def run(self):
        """
        Schedules the update using the index gotten by using the get_index method
        and then run  the process.
        :return:
        """
        index, index_id = self.get_index()
        self.update(index, index_id)


if __name__ == '__main__':
    updater = Updater()
    updater.run()
