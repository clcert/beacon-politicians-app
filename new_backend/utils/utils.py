from utils.data import CURRENT_DEPUTIES_URL
from datetime import datetime, date, timedelta
from bs4 import BeautifulSoup
import requests

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
        return datetime(year=date.year, month=date.month, day=date.day)
    return datetime(
        year=date.year, month=date.month, day=date.day,
        hour=time.hour, minute=time.minute
    )

def get_today_timestamp():
    """
    Gets the timestamp for today at 00:00:00 UTC-3.
    :return: timestamp.
    """
    dt_utc = datetime.utcnow()
    dt_local = datetime.now()

    today_pulse = dt_utc.day > dt_local.day or (
        dt_utc.day == dt_local.day and dt_utc.hour >= 4
    )

    today = date.today() if today_pulse else date.today() - timedelta(days=1)

    [year, month, day] = str(today).split('-')
    timestamp = datetime(year=int(year), month=int(month), day=int(day), hour=0, minute=0)

    return timestamp


def showSummary(profile, datetime, chainId, pulseId):
    pulseUri = f"https://random.uchile.cl/beacon/2.0-beta1/chain/{chainId}/pulse/{pulseId}"
    print("----------------------------------------")
    print("Resultados para el día", datetime.strftime("%d/%m/%Y"))
    print("Diputado Escogido:", profile['first_name'], profile['first_surname'])
    print("Partido:", profile['party'])
    print("Región:", profile['district_region'])
    print("Distrito:", profile['district'])
    print("Elegido en base al pulso:", pulseUri)
    print("----------------------------------------")
