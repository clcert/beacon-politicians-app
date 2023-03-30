# selenium
from selenium import webdriver
from datetime import datetime
from time import perf_counter

from threading import Thread, Lock

# drivers
from drivers.drivers import chromium_driver, google_chrome_driver

# deputies
from deputies.deputy import DeputyParser
from deputies.utils import get_number_of_deputies, get_json_data
from deputies.parsers.expenses import (
    OfficesExpensesParser,
    OperationalExpensesParser,
    StaffExpensesParser,
)

# settings
from settings import JsonFiles, FILE_LOCATIONS

import json

deputies_expenses = []
THREADS = 4


def parse_expenses(profile, driver):
    """
    Function that gets the expenses of a deputy in the last 5 months.
    :return: Returns a dictionary containing 
        - Operational expenses
        - Offices expenses
        - Staff expenses
    """
    # Measure elapsed time
    t_init = perf_counter()

    parsers = {
        'operational': OperationalExpensesParser,
        'offices': OfficesExpensesParser,
        'staff': StaffExpensesParser,
    }

    all_expenses = {}

    for expense_name, parser in parsers.items():
        current_parser = parser(profile, driver=driver)
        expenses_data = current_parser.get_deputy_expenses()
        deputy_id_str = f'{profile["index"]} - {profile["first_name"]} {profile["first_surname"]}'
        if expenses_data == []:
            print(f'[{deputy_id_str}] {expense_name.capitalize()} Expenses: not found.')
        else:
            print(f'[{deputy_id_str}] {expense_name.capitalize()} Expenses: obtained.')
        all_expenses[expense_name] = expenses_data

    # Show summary
    print(f'[{deputy_id_str}] Elapsed time: ', round(perf_counter() - t_init, 3), 's', end='\n\n')
    
    return all_expenses


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless") # We don't need a GUI

    driver = chromium_driver(options)
    if driver:
        return driver
    else:
        return google_chrome_driver(options)


def create_file():
    with open(FILE_LOCATIONS[JsonFiles.EXPENSES], 'w') as f:
        f.write('')
    

def save_deputy_expenses(deputy_profile):
    data = get_json_data(JsonFiles.EXPENSES)
    if data is None:
        data = {'expenses': [], 'last_update': ''}
    data['expenses'].append(deputy_profile)
    data['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    file_path = FILE_LOCATIONS[JsonFiles.EXPENSES]

    with open(file_path, 'w', encoding='utf-8') as expenses_file:
        try:
            json.dump(data, expenses_file, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f'Error saving expenses: \n{e}')
        finally:
            expenses_file.close()


def parse_deputies_expenses(writer_lock, indexes_list):
    driver = get_driver()

    if driver is None:
        print('Failed to run chrome driver.')
        print('Index list: ', ', '.join(indexes_list))
        return

    for local_index in indexes_list:
        current_deputy = DeputyParser(index=local_index)
        deputy_profile = current_deputy.get_profile()
        deputy_profile['index'] = local_index
        deputy_profile['expenses'] = parse_expenses(deputy_profile, driver)
        with writer_lock:
            save_deputy_expenses(deputy_profile)        
    
    driver.close()


def sort_expenses_by_deputy_index():
    data = get_json_data(JsonFiles.EXPENSES)
    expenses = data['expenses']
    sorted_expenses = sorted(expenses, key=lambda x: x['index'])
    data['expenses'] = sorted_expenses

    file_path = FILE_LOCATIONS[JsonFiles.EXPENSES]

    with open(file_path, 'w', encoding='utf-8') as expenses_file:
        json.dump(data, expenses_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    total_deputies = get_number_of_deputies()
    indexes_list = list(range(total_deputies))

    create_file()

    # create a shared lock
    writer_lock = Lock()

    threads_list = []
    for i in range(THREADS):
        thread = Thread(target=parse_deputies_expenses, args=(writer_lock, indexes_list[i::THREADS],))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    sort_expenses_by_deputy_index()
