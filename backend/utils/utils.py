from utils.data import OPENDATA_CAMARA_URL, CURRENT_DEPUTIES_URL, DEPUTIES_JSON_PATH
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
from os import path, stat

import json
import requests

CURRENT_LEGISLATURE_URL = OPENDATA_CAMARA_URL + 'WSLegislativo.asmx/retornarLegislaturaActual'
UTC_CHILE = -3 # UTC-3 summer time

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

def get_number_of_deputies():
    """
    Method used to get the total number of deputies on the current legislature.
    :return: Returns the total number of deputies as an integer.
    """
    response = requests.get(CURRENT_DEPUTIES_URL)
    soup = BeautifulSoup(response.content, 'xml')

    deputies = soup.find_all('Diputado')
    return len(deputies)

def get_current_month():
    return datetime.now().month

def get_current_year():
    return datetime.now().year

def get_datetime_from_epoch(epoch):
    return datetime.fromtimestamp(epoch)

def get_datetime_from_date_and_time(date, time):
    if not time:
        return datetime(year=date.year, month=date.month, day=date.day, hour=get_hrs_diff(), minute=0)
    return datetime(
        year=date.year, month=date.month, day=date.day,
        hour=time.hour, minute=time.minute
    )

def get_hrs_diff():
    """
    Gets the difference between the local time and the UTC time.
    :return: Returns the difference in hours as an integer.
    """
    dt_utc = datetime.utcnow()
    dt_local = datetime.now()

    return (dt_local.hour - dt_utc.hour - UTC_CHILE) % 24

def get_today_timestamp():
    """
    Gets the timestamp for today at 00:00:00 UTC-3.
    :return: timestamp.
    """
    dt_utc = datetime.utcnow()
    dt_local = datetime.now()

    today_pulse = dt_utc.day > dt_local.day or (
        dt_utc.day == dt_local.day and dt_utc.hour >= (-UTC_CHILE)
    )

    today = date.today() if today_pulse else date.today() - timedelta(days=1)

    [year, month, day] = str(today).split('-')
    timestamp = datetime(year=int(year), month=int(month), day=int(day), hour=get_hrs_diff(), minute=0)

    return timestamp


def get_json_data(file_path=DEPUTIES_JSON_PATH):
    """
    Returns an ordered list of dictionaries containing the date, index from the deputies list and the beacon id,
    ordered according to the date.
    :return:
    """    
    if path.exists(file_path) and stat(file_path).st_size != 0:
        with open(file_path, 'r', encoding='utf-8') as infile:
            try:
                json_data = json.load(infile)
                return json_data
            except (json.decoder.JSONDecodeError, ValueError) as err:
                print(err)
                return None
    return None


def showSummary(profile, datetime, chainId, pulseId):
    pulseUri = f"https://random.uchile.cl/beacon/2.1-beta/chain/{chainId}/pulse/{pulseId}"
    print("----------------------------------------")
    print("Resultados para el día", datetime.strftime("%d/%m/%Y"))
    print("Diputado Escogido:", profile['first_name'], profile['first_surname'])
    print("Partido:", profile['party'])
    print("Región:", profile['district_region'])
    print("Distrito:", profile['district'])
    print("Elegido en base al pulso:", pulseUri)
    print("----------------------------------------")
