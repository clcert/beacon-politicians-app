from bs4 import BeautifulSoup
from datetime import datetime
from utils.data import CURRENT_DEPUTIES_URL
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
    print("Main profiles updated.")

def update_expenses(from_id=0, to_id=get_number_of_deputies()):
    """
    Updates all deputy expenses.
    """
    print("Updating expenses...")
    for local_id in range(from_id, to_id):
        deputy_parser = DeputyParser(local_id)
        deputy_parser.load_or_update_profile()
        deputy_parser.update_deputy_expenses()
    print("Expenses updated.")

