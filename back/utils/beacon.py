from random import seed, randint
from utils.utils import DEPUTIES_NUM
from datetime import datetime
import requests


def get_local_index(pulse_randout):
    """
    Get a random number in the range of the deputies list length.
    :return: An integer in the range of the list described.
    """
    seed(pulse_randout)
    index = randint(0, DEPUTIES_NUM - 1)
    return index


def get_pulse_data(datetime: datetime):
    """
    Given a datetime object, gets its timestamp and return the beacon record and the output value.
    :param date_hour: Datetime object used to get the record and output value.
    :return:
    """
    url = 'https://random.uchile.cl/beacon/2.1-beta/pulse?timeGE=' + str(int(datetime.timestamp()) * 1000)
    try:
        page = requests.get(url)
        json_page = page.json()

        randOut = json_page['pulse']['outputValue']
        chainId = json_page['pulse']['chainIndex']
        pulseId = json_page['pulse']['pulseIndex']

        return (chainId, pulseId, randOut)
    except Exception as e:
        print(f"Fallo al obtener el pulso de Random UChile: {e}")
        return None