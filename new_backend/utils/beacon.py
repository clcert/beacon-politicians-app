from random import seed, randint
import requests

from utils.utils import get_number_of_deputies

def get_index(pulse_randout):
    """
    Get a random number in the range of the deputies list length.
    :return: An integer in the range of the list described.
    """
    seed(pulse_randout)
    index = randint(0, get_number_of_deputies() - 1)
    return index


def get_pulse_data(timestamp):
    """
    Given a datetime object, gets its timestamp and return the beacon record and the output value.
    :param date_hour: Datetime object used to get the record and output value.
    :return:
    """
    url = 'https://random.uchile.cl/beacon/2.0-beta1/pulse?time=' + str(int(timestamp.timestamp()) * 1000)
    page = requests.get(url)
    json_page = page.json()

    randOut = json_page['pulse']['outputValue']
    chainId = json_page['pulse']['chainIndex']
    pulseId = json_page['pulse']['pulseIndex']

    return (chainId, pulseId, randOut)
