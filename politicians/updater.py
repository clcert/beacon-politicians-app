import json
import datetime
import os
import parser.deputies as pd
import random
import requests
import argparse


class Updater:
    def __init__(self):
        self.json_path = os.path.dirname(os.path.realpath(__file__)) + '/static/json/deputies.json'

    def index_from_json(self, date_hour):
        url = 'https://beacon.clcert.cl/beacon/1.0/pulse/' + str(int(date_hour.timestamp()))
        page = requests.get(url)
        json_page = page.json()
        return json_page['outputValue'], json_page['id']

    def get_index(self, date_hour):
        """
        Get a random number in the range of the deputies list length.
        TO DO: Modify using CLCERT Beacon Random
        :return: An integer in the range of the list described.
        """
        max_index = pd.Parser().count_deputies() - 1

        index, record = self.index_from_json(date_hour)
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

    def update(self, using_json=True, date_hour=None):
        """
        Given an index for the position of the deputy at deputies list, modifies the json
        file using deputy's information.
        :param; Boolean used for testing, must be True for update in json and false if testing.
        :return:
        """
        if not date_hour:
            url = 'https://beacon.clcert.cl/beacon/1.0/pulse/last'
            page = requests.get(url)
            date_hour = datetime.datetime.fromtimestamp(page.json()['time'])

        index, record = self.get_index(date_hour)
        if using_json:
            with open(self.json_path, 'r', encoding='utf-8') as infile:
                try:
                    deputies = json.load(infile)
                except ValueError:
                    deputies = dict(deputies=list())
                finally:
                    infile.close()

            with open(self.json_path, 'w', encoding='utf-8') as outfile:
                deputy = dict(date=date_hour, index=index, record=record)

                deputies['deputies'].append(deputy)
                json.dump(deputies, outfile, ensure_ascii=False)

                outfile.close()
        else:
            parser = pd.Parser()
            deputy = parser.get_profile(parser.idfindex(index))
            print('Record: ', record)
            print('Fecha: ', date_hour)
            print('Indice obtenido: ', index)
            print('Diputado: ', deputy['first_name'], deputy['first_surname'])

        return

    def run(self):
        """
        Updates using the index gotten by using the get_index method
        and then run  the process.
        :return:
        """
        self.update()


def valid_date(date):
    try:
        return datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date)
        raise argparse.ArgumentTypeError(msg)


def valid_hour(hour):
    try:
        return datetime.datetime.strptime(hour, "%H:%M")
    except ValueError:
        msg = "Not a valid hour: '{0}'.".format(hour)
        raise argparse.ArgumentTypeError(msg)


if __name__ == '__main__':
    description = "By default, gets and updates information for the last deputy, or print it. Also, given a date and " \
                  "hour in specific, can get information of the deputy that should be obtained by using the correspo" \
                  "nding record of that date."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-p", "--print",
                        help="Display information of the deputy.",
                        action="store_true")
    parser.add_argument("-d", "--date",
                        help="Sets the date to get the record, by default at 00:00 hrs, if hour isn't specified. "
                             "Format must be YYYY-mm-dd",
                        type=valid_date)
    parser.add_argument("-t", "--time",
                        help="Sets the hour to get the record, by default using the current date if date isn't "
                             "specified. Format must be HH:MM",
                        type=valid_hour)
    parser.add_argument("-e", "--epoch",
                        help="Sets the date and time to the given epoch. If date or time are given, will prioritize"
                             "the epoch argument.",
                        type=int)

    args = parser.parse_args()

    if not args.print:
        updater = Updater()
        updater.run()

    else:
        if args.epoch:
            date = datetime.datetime.fromtimestamp(args.epoch)

        else:
            url = 'https://beacon.clcert.cl/beacon/1.0/pulse/last'
            page = requests.get(url)

            date = datetime.datetime.fromtimestamp(page.json()['time'])
            if args.date:
                date = datetime.datetime(year=args.date.year, month=args.date.month, day=args.date.day)
            if args.time:
                date = datetime.datetime(year=date.year, month=date.month, day=date.day,
                                         hour=args.time.hour, minute=args.time.minute)

        updater = Updater()
        updater.update(using_json=False, date_hour=date)
