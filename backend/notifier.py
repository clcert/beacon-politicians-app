from datetime import datetime
from random import seed, randint
from utils.db import find_deputy_for_date
from utils.utils import get_number_of_deputies
from utils.utils import get_json_data
from deputies.parser import DeputyParser

import requests


def check_todays_deputy_in_db():
    """
    Checks if the deputy of the day is already saved in the database.
    """
    today = datetime.today().strftime('%Y-%m-%d')
    return find_deputy_for_date( today + ' 00:00:00')

def main():
    db_data = check_todays_deputy_in_db()
    if not db_data:
        print('No deputy for today')

    (deputy_id, chain_id, pulse_id, randOut) = db_data
    response = requests.get(f'https://random.uchile.cl/beacon/2.0-beta1/chain/{chain_id}/pulse/{pulse_id}').json()
    pulse = response['pulse']
    pulseRandOut = pulse['outputValue']

    if randOut != pulseRandOut:
        print('The deputy is not the same as the one in the database')

    seed(pulseRandOut)
    index = randint(0, get_number_of_deputies() - 1)
    parser = DeputyParser(index)

    if parser.real_index != deputy_id:
        print('The deputy is not the same as the one in the database')

    json_data = get_json_data()
    deputies = json_data['records']
    deputy = list(filter(lambda x: x['index'] == deputy_id, deputies))
    if not deputy:
        print('The deputy is not in the JSON file')
    
    print('The deputy is the same as the one in the database and in the JSON file')


if __name__ == '__main__':
    main()