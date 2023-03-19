from argparse import ArgumentParser
from datetime import datetime, date
from pytz import timezone, utc
from time import sleep

import json

from settings import JSON_PATH
from deputies.deputy import DeputyParser
from deputies.updater.beacon import get_pulse_data, get_index
from deputies.utils import (
    valid_date,
    valid_hour,
    create_path_if_not_exists,
    get_json_data
)


def collect_deputy_info(timestamp=None, only_print=False):
    """
    Collects info from a random deputy and saves it in a json file.
    :param date_hour: datetime object to get the pulse data.
    :param only_print: if true only prints basic info.
    :return:
    """
    if timestamp is None:
        [year, month, day] = str(date.today()).split('-')
        timestamp = datetime(year=int(year), month=int(month), day=int(day), hour=0, minute=0)

    # Convert to UTC time
    local_dt = timezone('America/Santiago').localize(timestamp, is_dst=None)
    timestamp = local_dt.astimezone(utc)

    chainId, pulseId, randOut = get_pulse_data(timestamp)
    local_index = get_index(randOut)

    print('---------------------')
    print('Pulse Index:', pulseId)
    print('Pulse Date:', timestamp.strftime("%Y-%m-%d %H:%M:%S"), 'UTC')
    print('Deputy Index:', local_index)
    print('---------------------')

    create_path_if_not_exists(JSON_PATH)

    # Only print the deputy information if not using json.
    if only_print:
        deputy = DeputyParser(local_index)
        profile = deputy.get_profile()
        print('Deputy: ', profile['first_name'], profile['first_surname'])
        return

    deputies = get_json_data()
    if deputies is None:
        deputies = dict(deputies=list())
    
    deputy = dict(
        date=timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        index=local_index,
        record=pulseId,
    )

    attempts = 0
    while attempts < 3:
        print(f'\n -- Attempt {attempts + 1}/3 -- \n')
        try:
            deputy = {**deputy, **DeputyParser(local_index).get_data()}
            deputies['deputies'] = save_or_update(deputies['deputies'], deputy)
            with open(JSON_PATH, 'w', encoding='utf-8') as outfile:
                json.dump(deputies, outfile, ensure_ascii=False)
                outfile.close()
            break
        except Exception as e:
            attempts += 1
            print(f'Unexpected error getting deputy information: {e}', end='\n\n')
            sleep(60)             

        return

def save_or_update(deputies_list, deputy):
    """
    Saves or updates the new deputy in the list of deputies.
    :param deputies_list: list of deputies.
    :param deputy: deputy to save or update.

    """
    deputies_list = list(filter(
        lambda d: d['date'] != deputy['date'] and d['index'] != deputy['index'],
        deputies_list
    ))
    deputies_list.append(deputy)
    deputies_list = deputies_list[-10:]

    return deputies_list


if __name__ == '__main__':
    # Declares Argument Parser using the description defined above.
    description = (
        "By default, gets and updates information for the last deputy, or print it. Also, given a date and " \
        "hour in specific, can get information of the deputy that should be obtained by using the correspo" \
        "nding record of that date."
    )
    parser = ArgumentParser(description=description)

    # Defines the different arguments
    parser.add_argument(
        "-p",
        "--print",
        help="Display information of the deputy.",
        action="store_true"
    )
    parser.add_argument(
        "-d",
        "--date",
        help=(
            "Sets the date to get the record, by default at 00:00 hrs, if hour isn't specified. "
            "Format must be YYYY-mm-dd"
        ),
        type=valid_date
    )
    parser.add_argument(
        "-t",
        "--time",
        help=(
            "Sets the hour to get the record, by default using the current date if date isn't "
            "specified. Format must be HH:MM",
        ),
        type=valid_hour
    )
    parser.add_argument(
        "-e",
        "--epoch",
        help=(
            "Sets the date and time to the given epoch. If date or time are given, will prioritize"
            "the epoch argument."
        ),
        type=int
    )

    args = parser.parse_args()
    
    if args.epoch:
        timestamp = datetime.fromtimestamp(args.epoch)

    elif args.date:
        timestamp = datetime.datetime(
            year=args.date.year, 
            month=args.date.month, 
            day=args.date.day
        )

        if args.time: # also include time
            timestamp = datetime.datetime(
                year=timestamp.year, 
                month=timestamp.month, 
                day=timestamp.day,
                hour=args.time.hour, 
                minute=args.time.minute
            )

    else:
        # If no arguments are given, use today at 00:00 hrs.
        timestamp=None

    # If print argument isn't given. Just update the json, with the last pulse.
    collect_deputy_info(timestamp=timestamp, only_print=args.print)
