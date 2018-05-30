import json
import datetime
import os
import parser.deputies as pd
import random
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

        index, record = self.index_from_json()
        random.seed(index)

        return random.randint(0, max_index), record

    def get_list(self):
        """
        Returns an ordered list of dictionaries containing the date, index from the deputies list and the beacon id,
        ordered according to the date.
        :return:
        """
        with open(self.json_path, 'r', encoding='utf-8') as infile:
            deputies_list = json.load(infile)['deputies']
            deputies_list = sorted(deputies_list, key=lambda k: datetime.datetime.strptime(k['date'],
                                                                                           "%Y-%m-%d %H:%M:%S"))
            return deputies_list

    def update(self):
        """
        Given an index for the position of the deputy at deputies list, modifies the json
        file using deputy's information.
        :return:
        """
        index, record = self.get_index()
        with open(self.json_path, 'r', encoding='utf-8') as infile:
            try:
                deputies = json.load(infile)
            except ValueError:
                deputies = dict(deputies=list())
            finally:
                infile.close()

        with open(self.json_path, 'w', encoding='utf-8') as outfile:
            modified = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            deputy = dict(date=modified, index=index, record=record)

            deputies['deputies'].append(deputy)
            json.dump(deputies, outfile, ensure_ascii=False)

            outfile.close()
        return

    def run(self):
        """
        Updates using the index gotten by using the get_index method
        and then run  the process.
        :return:
        """
        self.update()


if __name__ == '__main__':
    updater = Updater()
    updater.run()
