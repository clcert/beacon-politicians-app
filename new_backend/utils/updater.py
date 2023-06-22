from bs4 import BeautifulSoup
from datetime import datetime
from utils.data import CURRENT_DEPUTIES_URL
from utils.db import insert_deputy_profile, insert_parlamentary_period
from deputies.deputy_parser import DeputyParser
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

def update_all_profiles():
    """
    Updates all deputy profiles.
    """
    print("Updating main profiles...")
    for local_id in range(get_number_of_deputies()):
        deputy_parser = DeputyParser(local_id)
        main_profile_dict = deputy_parser.update_profile()
        main_profile_dict['last_update'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        insert_deputy_profile(main_profile_dict)
        for period in main_profile_dict['periods']:
            period_from, period_to = period.split('-')
            insert_parlamentary_period({
                'id': main_profile_dict['id'],
                'period_from': int(period_from),
                'period_to': int(period_to),
            })

    print("Main profiles updated.")

