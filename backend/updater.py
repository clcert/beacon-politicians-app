import json
import datetime
import os
import parser.deputies as pd
import random
import requests
import argparse
import pytz


class Updater:
    def __init__(self):
        self.json_path = os.path.dirname(os.path.realpath(__file__)) + '/json/deputies.json'

    def index_from_json(self, date_hour):
        """
        Given a datetime object, gets its timestamp and return the beacon record and the output value.
        :param date_hour: Datetime object used to get the record and output value.
        :return:
        """
        url = 'https://random.uchile.cl/beacon/2.0-beta1/pulse/time/' + str(int(date_hour.timestamp()) * 1000)
        page = requests.get(url)
        json_page = page.json()

        return json_page['pulse']['outputValue'], json_page['pulse']['pulseIndex']

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
        if os.stat(self.json_path).st_size != 0:
            with open(self.json_path, 'r', encoding='utf-8') as infile:
                try:
                    deputies_list = json.load(infile)['deputies']
                    deputies_list = sorted(deputies_list, key=lambda k: datetime.datetime.strptime(k['date'],
                                                                                                   "%Y-%m-%d %H:%M:%S"))
                    return deputies_list
                except ValueError:
                    return None

    def update(self, using_json=True, date_hour=None):
        """
        Given an index for the position of the deputy at deputies list, modifies the json
        file using deputy's information.
        :param; Boolean used for testing, must be True for update in json and false if testing.
        :return:
        """
        json_index = 0
        if self.get_list() != None:
            json_index = len(self.get_list())

        if not date_hour:
            [year, month, day] = str(datetime.date.today()).split('-')
            date_hour = datetime.datetime(year=int(year), month=int(month), day=int(day), hour=0, minute=0)

        # Convert to UTC time
        local_dt = pytz.timezone('America/Santiago').localize(date_hour, is_dst=None)
        date_hour = local_dt.astimezone(pytz.utc)

        index, record = self.get_index(date_hour)

        print('---------------------')
        print('Record:', record)
        print('Pulse Date:', date_hour.strftime("%Y-%m-%d %H:%M:%S"), 'UTC')
        print('Deputy Index:', index)
        print('---------------------')

        if using_json:
            with open(self.json_path, 'r', encoding='utf-8') as infile:
                try:
                    deputies = json.load(infile)
                except ValueError:
                    deputies = dict(deputies=list())
                finally:
                    infile.close()

            with open(self.json_path, 'w', encoding='utf-8') as outfile:
                deputy = dict(
                    date=date_hour.strftime("%Y-%m-%d %H:%M:%S"),
                    index=index,
                    record=record,
                    json_index=json_index
                )
                # If something goes wrong, the json file is not modified.
                try:
                    deputy = {**deputy, **pd.Parser().get_deputy(index)}
                    deputies['deputies'].append(deputy)
                    # Keeps only the last 7 deputies
                    deputies['deputies'] = deputies['deputies'][-7:]
                    print(f'Done.\n\n\n')
                except Exception as e:
                    print(e)
                    print(f'Unexpected error getting deputy information.\n\n\n')
                finally:
                    json.dump(deputies, outfile, ensure_ascii=False)
                    outfile.close()
        else:
            parser = pd.Parser()
            deputy = parser.get_profile(parser.idfindex(index))
            print('Deputy: ', deputy['first_name'], deputy['first_surname'])

        return

    def run(self):
        """
        Updates using the index gotten by using the get_index method
        and then run  the process.
        :return:
        """
        self.update()


def valid_date(date):
    """
    Checks if a date is valid according to the argument parser.
    :param date: String representing a date. Format must be YYYY-mm-dd.
    :return: Datetime object representing the given string.
    """
    try:
        return datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date)
        raise argparse.ArgumentTypeError(msg)


def valid_hour(hour):
    """
    Checks if an hour is valid according to the argument parser.
    :param hour: String representing an hour. Format must be HH:MM.
    :return: Datetime object representing te given string.
    """
    try:
        return datetime.datetime.strptime(hour, "%H:%M")
    except ValueError:
        msg = "Not a valid hour: '{0}'.".format(hour)
        raise argparse.ArgumentTypeError(msg)


if __name__ == '__main__':
    # Declares Argument Parser using the description defined above.
    description = "By default, gets and updates information for the last deputy, or print it. Also, given a date and " \
                  "hour in specific, can get information of the deputy that should be obtained by using the correspo" \
                  "nding record of that date."
    parser = argparse.ArgumentParser(description=description)

    # Defines the different arguments
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

    
    if args.epoch:
        date = datetime.datetime.fromtimestamp(args.epoch)

    elif args.date:
        date = datetime.datetime(
            year=args.date.year, 
            month=args.date.month, 
            day=args.date.day
        )

        if args.time: # also include time
            date = datetime.datetime(
                year=date.year, 
                month=date.month, 
                day=date.day,
                hour=args.time.hour, 
                minute=args.time.minute
            )

    else:
        date = None

    # If print argument isn't given. Just update the json, with the last pulse.
    # Else, checks for the different arguments, and asks for the information according to the documentation.s
    updater = Updater()
    updater.update(using_json=(not args.print), date_hour=date)
