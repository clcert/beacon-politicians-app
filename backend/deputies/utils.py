from bs4 import BeautifulSoup
from argparse import ArgumentTypeError
from datetime import datetime, date, timedelta
from os import path, stat

import requests
import json

from settings import (
    ALL_LEGISLATURES_URL,
    CURRENT_LEGISLATURE_URL,
    CURRENT_DEPUTIES_URL,
    FILE_LOCATIONS,
    JsonFiles,
)   

def get_number_of_deputies():
    """
    Method used to get the total number of deputies on the current legislature.
    :return: Returns the total number of deputies as an integer.
    """
    response = requests.get(CURRENT_DEPUTIES_URL)
    soup = BeautifulSoup(response.content, 'xml')

    deputies = soup.find_all('Diputado')
    return len(deputies)


def get_current_legislature():
    """
    Obtains the information from the latest legislature.
    :return: Returns a dictionary containing the id of the latest legislature, and the date of end and start
        as a datetime object.
    """
    response = requests.get(CURRENT_LEGISLATURE_URL)
    soup = BeautifulSoup(response.content, 'xml')

    legislature_id = int(soup.find('Id').get_text().strip())

    start = soup.find('FechaInicio').get_text()
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")

    end = soup.find('FechaTermino').get_text()
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

    legislature = dict(id=legislature_id, start=start, end=end)

    return legislature


def get_previous_legislature_id():
    """
    Obtains the information from the previous legislature.
    :return: Returns a dictionary containing the id of the previous legislature, and the date of end and start
        as a datetime object.
    """
    response = requests.get(ALL_LEGISLATURES_URL)
    soup = BeautifulSoup(response.content, 'xml')

    prev_id = soup.find_all('Id')[-2].get_text().strip()

    return prev_id

def get_current_month():
    return datetime.now().month

def get_current_year():
    return datetime.now().year

def valid_date(date):
    """
    Checks if a date is valid according to the argument parser.
    :param date: String representing a date. Format must be YYYY-mm-dd.
    :return: Datetime object representing the given string.
    """
    try:
        return datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(date)
        raise ArgumentTypeError(msg)


def valid_hour(hour):
    """
    Checks if an hour is valid according to the argument parser.
    :param hour: String representing an hour. Format must be HH:MM.
    :return: Datetime object representing te given string.
    """
    try:
        return datetime.strptime(hour, "%H:%M")
    except ValueError:
        msg = "Not a valid hour: '{0}'.".format(hour)
        raise ArgumentTypeError(msg)

def check_json_correct_format(json_file=JsonFiles.DEPUTIES):
    """
    Checks if the file format is correct as a json file
    :return: True if the file is formatted as a json, else False
    """
    if json_file == JsonFiles.DEPUTIES:
        file_path = FILE_LOCATIONS[JsonFiles.DEPUTIES]
    elif json_file == JsonFiles.EXPENSES:
        file_path = FILE_LOCATIONS[JsonFiles.EXPENSES]
    else:
        raise ValueError('Invalid json file')
    
    if not path.exists(file_path):
        print(file_path + ' does not exist')
        return False

    with open(file_path, 'r') as infile:
        try:
            # Try to load the file as json
            json.load(infile)  
        except (json.decoder.JSONDecodeError, ValueError) as err:
            print(err)
            return False
        finally:
            infile.close()
        return True

def get_json_data(json_file=JsonFiles.DEPUTIES):
    """
    Returns an ordered list of dictionaries containing the date, index from the deputies list and the beacon id,
    ordered according to the date.
    :return:
    """
    if json_file == JsonFiles.DEPUTIES:
        file_path = FILE_LOCATIONS[JsonFiles.DEPUTIES]
    elif json_file == JsonFiles.EXPENSES:
        file_path = FILE_LOCATIONS[JsonFiles.EXPENSES]
    else:
        raise ValueError('Invalid json file')
    
    if path.exists(file_path) and stat(file_path).st_size != 0:
        with open(file_path, 'r', encoding='utf-8') as infile:
            try:
                json_data = json.load(infile)
                return json_data
            except (json.decoder.JSONDecodeError, ValueError) as err:
                print(err)
                return None
    return None


def get_sorted_deputies():
    """
    Returns a list of dictionaries containing the date, index from the deputies list and the beacon id,
    ordered according to the date.
    :return:
    """
    json_data = get_json_data()
    if json_data is not None:
        deputies_list = json_data['deputies']
        sorted_deputies_list = sorted(
            deputies_list, 
            key=lambda k: datetime.strptime(
                k['date'],
                "%Y-%m-%d %H:%M:%S"
            )
        )
        return sorted_deputies_list
    return []


def create_path_if_not_exists(check_path):
    """
    Creates a path if it does not exist.
    :param path: Path to be created.
    :return:
    """
    # if the json file does not exist, create it.
    if not path.exists(check_path):
        dep_json = open(check_path, "x")
        dep_json.close()


def get_today_timestamp():
    """
    Gets the timestamp for today at 00:00:00 UTC-3.
    :return: timestamp.
    """
    dt_utc = datetime.utcnow()
    dt_local = datetime.now()

    today_pulse = dt_utc.day > dt_local.day or (
        dt_utc.day == dt_local.day and dt_utc.hour >= 3
    )

    if today_pulse:
        today = date.today()
    else:
        today = date.today() - timedelta(days=1)

    [year, month, day] = str(today).split('-')
    timestamp = datetime(year=int(year), month=int(month), day=int(day), hour=0, minute=0)

    return timestamp
