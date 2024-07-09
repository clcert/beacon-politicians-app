from collectors.access_points import OpenDataAPI
from datetime import datetime
from pytz import timezone, UTC
from bs4 import BeautifulSoup
import requests


DEPUTIES_NUM = 155

MONTHS = [
    "enero",    "febrero",  "marzo",        "abril",    "mayo",         "junio", 
    "julio",    "agosto",   "septiembre",   "octubre",  "noviembre",    "diciembre",
]

JSON_PATH = "deputies.json"

def get_current_month():
    return datetime.now().month

def get_current_year():
    return datetime.now().year

def get_midnight_timestamp(date: datetime) -> datetime:
    return datetime(year=date.year, month=date.month, day=date.day, hour=get_hrs_diff(), minute=0)

def get_hrs_diff():
    """
    Gets the difference between the chilean time and the UTC time.
    :return: Returns the difference in hours as an integer.
    """
    dt_utc = datetime.now(tz=UTC)
    dt_local = datetime.now(timezone("America/Santiago"))

    return (dt_utc.hour - dt_local.hour) % 24

def get_current_legislature():
    """
    Obtains the information from the latest legislature.
    :return: Returns a dictionary containing the id of the latest legislature, and the date of end and start
        as a datetime object.
    """
    response = requests.get(OpenDataAPI.current_legislature)
    soup = BeautifulSoup(response.content, 'xml')

    legislature_id = int(soup.find('Id').get_text().strip())

    start = soup.find('FechaInicio').get_text()
    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")

    end = soup.find('FechaTermino').get_text()
    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")

    legislature = dict(id=legislature_id, start=start, end=end)

    return legislature