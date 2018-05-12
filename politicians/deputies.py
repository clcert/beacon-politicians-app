import parser.deputies as pd
import os
import json
from datetime import datetime
from datetime import timedelta


class Deputies:
    def __init__(self):
        self.json_path = os.getcwd() + '/static/json/deputies.json'

        # Sets duration of the time interval
        self.time_interval = timedelta(minutes=1)

        # Time of last modification and deputies list
        self.modified, self.list = self.update()

    def update(self):
        """
        Gets the latest date and time json's modification. If the time elapsed
        between the modification gotten and the current time is greater than the
        defined time interval, updates json and returns the new modification.
        :return:
        """

        need_modify = False
        modified = None
        deputies_list = dict()
        current = dict()

        # Checks for latest modification
        with open(self.json_path, 'r') as infile:
            try:
                dict_deputies = json.load(infile)
                if dict_deputies["modified"]:
                    modified = dict_deputies["modified"]
                    modified = datetime.strptime(modified, "%Y-%m-%d %H:%M:%S.%f")

                    if dict_deputies["deputies"]:
                        deputies_list = dict_deputies["deputies"]

                    if dict_deputies["current"]:
                        current = dict_deputies["current"]

                    need_modify = datetime.now() - modified > self.time_interval

            # There is an error with the file, so needs modification
            except ValueError:
                need_modify = True

            finally:
                infile.close()

        if need_modify:
            dict_deputies = pd.Parser().get_deputies()

            # Writes new json with updated info
            with open(self.json_path, 'w') as outfile:
                modified = dict_deputies["modified"]
                modified = datetime.strptime(modified, "%Y-%m-%d %H:%M:%S.%f")

                deputies_list = dict_deputies["deputies"]

                # If there is a current deputy saved, we don't change it
                if current:
                    dict_deputies["current"] = current

                json.dump(dict_deputies, outfile)
                outfile.close()

        return modified, deputies_list

