# selenium
from selenium import webdriver
from datetime import datetime
from time import perf_counter
from statistics import mean, stdev

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
from settings import JsonFiles, FILE_LOCATIONS, OP_EXPENSES_TYPES

import json

deputies_expenses = []
THREADS = 2


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
    """
    Function that returns a driver to be used in the parsing process.
    :return: Returns a driver.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless") # We don't need a GUI

    driver = chromium_driver(options)
    if driver:
        return driver
    else:
        return google_chrome_driver(options)


def create_file():
    """
    Function that creates the expenses file if it doesn't exist.
    """
    with open(FILE_LOCATIONS[JsonFiles.EXPENSES], 'w') as f:
        f.write('{ expenses: "", last_update: "" }')
    

def save_deputy_expenses(deputy_profile):
    """
    Function that saves the expenses of a deputy in the expenses file.
    :param deputy_profile: Dictionary containing the expenses of a deputy.
    """
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
    """
    Function that parses the expenses of a list of deputies.
    :param writer_lock: Lock to be used when writing to the expenses file.
    :param indexes_list: List of indexes of the deputies to be parsed.
    """
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

def get_month_data(deputies_expenses, expense_type, month):
    """
    Function that gets the expenses of a given month and expense type.
    :param deputies_expenses: List of dictionaries containing the expenses of each deputy.
    :param expense_type: Type of expenses to be filtered.
    :param month: Month to be filtered.
    :return: Returns a list of dictionaries containing the expenses of each deputy.
    """
    # get deputies expenses data
    deputies_data = map(
        lambda deputy: deputy['expenses'][expense_type],
        deputies_expenses
    )
    # filter by month
    month_data = map(
        lambda deputy_operational: 
            next(filter(
                lambda deputy_operational_month: deputy_operational_month['month'] == month,
                deputy_operational,
            )),
        deputies_data,
    )
    return list(month_data)


def get_operational_detail(month_data):
    """
    Function that gets the operational detail of a given month.
    :param month_data: List of dictionaries containing the expenses of each deputy.
    :return: Returns a dictionary containing the average expenses of each category.
    """
    month_operational_detail = {}

    for category in OP_EXPENSES_TYPES:
        total_avg = round(mean(map(lambda x: x[category], month_data)))
        total_std = round(stdev(map(lambda x: x[category], month_data)))
        month_operational_detail[category] = {
            'total': total_avg,
            'total_std': total_std,
        }

    return month_operational_detail

def compute_average_expenses(deputies_expenses):
    """
    Computes the average expenses of all deputies.
    :param expenses: List of dictionaries containing the expenses of each deputy.
    :return: Dictionary containing the average expenses of each category.
    """

    average_expenses_dict = {
        'operational': {},
        'offices': {},
        'staff': {},
    }

    first_deputy_expenses = deputies_expenses[0]['expenses']
    months = {
        'operational': list(map(lambda x: x['month'], first_deputy_expenses['operational'])),
        'offices': list(map(lambda x: x['month'], first_deputy_expenses['offices'])),
        'staff': list(map(lambda x: x['month'], first_deputy_expenses['staff'])),
    }

    for expense_type in average_expenses_dict.keys():
        average_expenses_dict[expense_type] = []

        for month in months[expense_type]:
            month_data = get_month_data(deputies_expenses, expense_type, month)

            month_operational_detail = None
            if expense_type == 'operational':
                month_operational_detail = get_operational_detail(month_data)

            total_avg = round(mean(map(lambda x: x['total'], month_data)))
            total_std = round(stdev(map(lambda x: x['total'], month_data)))

            average_expenses_dict[expense_type].append({
                'total': total_avg,
                'total_std': total_std,
                'month': month,
                'detail': month_operational_detail,
            })

    return average_expenses_dict


def add_avg_and_sort():
    """
    Function that adds the average expenses to the expenses file and sorts the expenses by index.
    """
    data = get_json_data(JsonFiles.EXPENSES)
    expenses = data['expenses']
    sorted_expenses = sorted(expenses, key=lambda x: x['index'])
    data['expenses'] = sorted_expenses
    data['average_expenses'] = compute_average_expenses(sorted_expenses)

    file_path = FILE_LOCATIONS[JsonFiles.EXPENSES]

    with open(file_path, 'w', encoding='utf-8') as expenses_file:
        json.dump(data, expenses_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    total_deputies = get_number_of_deputies()
    indexes_list = list(range(total_deputies))

    create_file()

    writer_lock = Lock() # shared lock

    threads_list = []
    for i in range(THREADS):
        thread = Thread(target=parse_deputies_expenses, args=(writer_lock, indexes_list[i::THREADS],))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    add_avg_and_sort()
