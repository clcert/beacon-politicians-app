from updater import Updater
from deputies.utils import (
    check_json_correct_format,
    get_sorted_deputies,
)

class DeputyLoader:
    def __init__(self, local_index):
        self.index = local_index
        self.info = None
        self.load_info()

    def load_info(self):
        """
        Get deputy's information if the file is json formatted, else
        update the file and return the information.
        :return:
        """
        if check_json_correct_format():
            deputies = get_sorted_deputies()
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
