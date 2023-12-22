from utils.drivers import get_driver
from utils.utils import get_number_of_deputies, showSummary
from utils.beacon import get_index, get_pulse_data
from utils.webutils import generate_deputy_json_data
from deputies.parser import DeputyParser

from requests.exceptions import SSLError, ConnectTimeout

def update_all_profiles():
    """
    Updates all deputy profiles.
    """
    print("[Manager] Updating main profiles. This may take a while...")
    n_deputies = get_number_of_deputies()
    for local_id in range(n_deputies):
        if local_id % 10 == 0: print("[Manager] Progress: {}%".format(round(local_id/n_deputies*100,2)))
        deputy_parser = DeputyParser(local_id)
        deputy_parser.update_profile()
    print("[Manager] Main profiles updated.")


def update_expenses(from_id=0, to_id=get_number_of_deputies()):
    """
    Updates all deputy expenses.
    """
    driver = get_driver()
    for local_id in range(from_id, to_id):
        deputy_parser = DeputyParser(local_id)
        deputy_parser.load_or_update_profile()
        print("[Manager] Updating expenses...")
        deputy_parser.update_deputy_expenses(driver=driver)
        print("[Manager] Expenses updated.")
        print("[Manager] Updating legislative activity...")
        deputy_parser.update_legislative_activity(driver=driver)
        print("[Manager] Legislative activity updated.")
    driver.close()


def choose_deputy(timestamp, verify=False):
    """
    Method used to choose a deputy for a given timestamp and update its data.
    :param timestamp: Timestamp to choose a deputy for.
    :param verify: If True, only shows the chosen deputy without updating its data.
    :return: Returns the id of the chosen deputy.
    """
    print("[Manager] Choosing deputy for timestamp {} using Random UChile randomness beacon.".format(timestamp.strftime('%Y-%m-%d %H:%M')))
    (chainId, pulseId, randOut) = get_pulse_data(timestamp)
    local_index = get_index(randOut)

    deputy_parser = DeputyParser(
        index=local_index,
        chain_id=chainId,
        pulse_id=pulseId,
        rand_out=randOut,
    )
    
    if verify: 
        deputy_parser.update_profile(save=False)
        showSummary(deputy_parser.profile, timestamp, chainId, pulseId)
        return

    print("[Manager] Loading deputy profile...")
    deputy_parser.load_or_update_profile()
    try:
        print("[Manager] Updating deputy attendance...")
        deputy_parser.update_attendance()
        print("[Manager] Updating deputy votings...")    
        deputy_parser.get_last_votes()
    except ConnectTimeout:
        print("[Manager] Connection Timeout with deputies chamber API. Skipping attendance and votings update...")
    except SSLError:
        print("[Manager] SSL Certificate Verification Error in deputies chamber API. Skipping attendance and votings update...")
    except Exception as e:
        print("[Manager] Unknown error. Skipping attendance and votings update...")
        print(e)

    print("[Manager] Saving as #DiputadxDelDia...")
    deputy_parser.save_as_deputy_of_the_day(timestamp)

    expenses_recorded = deputy_parser.saved_deputy_expenses()
    activity_recorded = deputy_parser.saved_legislative_activity()
    if not expenses_recorded or not activity_recorded:
        try:
            driver = get_driver()
            if not expenses_recorded:
                print("[Manager] No expenses found for this deputy. Scraping expenses...")
                deputy_parser.update_deputy_expenses(driver=driver)
            if not activity_recorded:
                print("[Manager] No legislative activity found for this deputy. Scraping activity...")
                deputy_parser.update_legislative_activity(driver=driver)
            driver.close()
        except Exception as e:
            print("[Manager] Unknown error. Skipping expenses and activity update...")
            print(e)
    print("[Manager] Deputy updated, generating JSON data...")
    generate_deputy_json_data(deputy_parser, timestamp, chainId, pulseId)