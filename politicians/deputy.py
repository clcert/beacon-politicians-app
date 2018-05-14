import json
import os
import datetime
import random
import parser.deputies as pd


class Deputy:
    def __init__(self):
        self.json_path = os.path.dirname(os.path.realpath(__file__)) + '/static/json/deputies.json'

        # Sets duration of the time interval
        self.time_interval = datetime.timedelta(minutes=1)

        # TO DO: Change to beacon random
        self.index = random.randint(0, len(pd.Parser().parse_personalinfo()))
        self.info = self.update()

    def update(self):
        """
        Get the latest deputy according to index generated by random algorithm if
        only if the time interval between the latest modification and the current
        time is smaller than the defined time interval. Else, gets the saved data
        from json.
        :return:
        """

        need_modify = False
        dict_deputy = dict()

        # Checks for latest modification
        with open(self.json_path, 'r') as infile:
            try:
                dict_deputy = json.load(infile)
                if dict_deputy["modified"]:
                    modified = dict_deputy["modified"]
                    modified = datetime.datetime.strptime(modified, "%Y-%m-%d %H:%M:%S.%f")

                    need_modify = datetime.datetime.now() - modified > self.time_interval

            # There is an error with the file, so needs modification
            except ValueError:
                need_modify = True

            finally:
                infile.close()

        if need_modify:
            dict_deputy = pd.Parser().get_deputy(self.index)

            # Writes new json with updated info
            with open(self.json_path, 'w', encoding='utf-8') as outfile:
                modified = datetime.datetime.now()
                modified = str(modified)
                dict_deputy = dict(modified=modified, current=dict_deputy)
                json.dump(dict_deputy, outfile, ensure_ascii=False)
                outfile.close()
        return dict_deputy
