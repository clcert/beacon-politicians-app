from datetime import datetime
from utils.drivers import get_driver
from utils.utils import get_number_of_deputies, showSummary
from utils.beacon import get_index, get_pulse_data
from deputies.deputy_parser import DeputyParser
import requests


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
    driver = get_driver()
    for local_id in range(from_id, to_id):
        deputy_parser = DeputyParser(local_id)
        deputy_parser.load_or_update_profile()
        deputy_parser.update_deputy_expenses(driver=driver)
    print("Expenses updated.")


def choose_deputy(timestamp, verify=False):
    """
    Method used to choose a deputy for a given timestamp and update its data.
    :param timestamp: Timestamp to choose a deputy for.
    :param verify: If True, only shows the chosen deputy without updating its data.
    :return: Returns the id of the chosen deputy.
    """
    print("Choosing deputy for timestamp {} using Random UChile randomness beacon.".format(timestamp.strftime('%Y-%m-%d %H:%M')))
    (chainId, pulseId, randOut) = get_pulse_data(timestamp)
    local_index = get_index(randOut)
    deputy_parser = DeputyParser(local_index)
    if verify: 
        deputy_parser.update_profile(save=False)
        showSummary(deputy_parser.profile, timestamp, chainId, pulseId)
        return

    deputy_parser.update_profile()
    # deputy_parser.update_attendance()
    # deputy_parser.update_votings()
    # deputy_parser.save_as_deputy_of_the_day(timestamp)
