# selenium
from selenium import webdriver
from datetime import datetime
from time import perf_counter

import threading

# drivers
from drivers.drivers import chromium_driver, google_chrome_driver

# deputies
from deputies.deputy import DeputyParser
from deputies.utils import get_number_of_deputies
from deputies.parsers.expenses import (
    OfficesExpensesParser,
    OperationalExpensesParser,
    StaffExpensesParser,
)

deputies_expenses = []
THREADS = 6


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
        if expenses_data == []:
            print(f'[Expenses] {expense_name.capitalize()} Not found.')
        else:
            print(f'[Expenses] {expense_name.capitalize()} Obtained.')
        all_expenses[expense_name] = expenses_data

    # Show summary
    print('[Expenses] Obtained')
    print('[Expenses] Elapsed time: ', round(perf_counter() - t_init, 3), 's', end='\n\n')
    
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


def parse_deputies_expenses(indexes_list):
    global deputies_expenses
    driver = get_driver()

    if driver is None:
        print('[Expenses] Failed to run chrome driver.')
        print('Index list: ', ', '.join(indexes_list))
        return

    for local_index in indexes_list:
        current_deputy = DeputyParser(index=local_index)
        deputy_profile = current_deputy.get_profile()
        deputy_profile['expenses'] = parse_expenses(deputy_profile, driver)
        deputies_expenses.append(deputy_profile)
    
    driver.close()
    return deputies_expenses


if __name__ == '__main__':
    total_deputies = get_number_of_deputies()
    indexes_list = list(range(total_deputies))

    threads_list = []
    for i in range(THREADS):
        thread = threading.Thread(target=parse_deputies_expenses, args=(indexes_list[i::THREADS],))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    deputies_expenses = parse_deputies_expenses()
    dump_data = {'expenses': deputies_expenses, 'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

    with open('deputies_expenses.json', 'w') as f:
        json.dump(deputies_expenses, f, indent=4)