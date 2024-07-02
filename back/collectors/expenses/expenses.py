from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from utils.utils import get_current_month, get_current_year, MONTHS
from utils.drivers import get_driver
from time import sleep

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

MAX_MONTHS_LOOKUP = 6

class ExpensesCollector:
    def __init__(self, driver=None):        
        self.driver = driver if driver else get_driver()
        self.url = ''
        self.month_selector_id = ''
        self.expenses = []

    def close_driver(self):
        self.driver.quit()

    def get_deputy_expenses(self):
        logger.info(f'getting deputy {self.expense_name} expenses')
        # Get the expenses page
        self.driver.get(self.url)
        expenses = []
        change_year = False

        # Get the current month and year
        month_index = get_current_month()
        year = get_current_year()
        
        while len(expenses) < MAX_MONTHS_LOOKUP:
            if month_index == 0:
                change_year = True
                year -= 1
                if year < get_current_year() - 2:
                    return []

            month_index = (month_index - 1) % 12
            month = MONTHS[month_index]

            try:
                if change_year: # Only change year if necessary
                    year_selector = Select(self.driver.find_element(By.ID, self.year_selector_id))
                    year_selector.select_by_value(str(year)) # Set corresponding year
                    # year_selector.select_by_visible_text(str(year)) # Set corresponding year
                    change_year = False
                    sleep(1) # wait for page to load

                # Change month in form
                month_selector = Select(self.driver.find_element(By.ID, self.month_selector_id))
                month_selector.select_by_visible_text(month) # Set corresponding month

                sleep(1) # wait for page to load
            except NoSuchElementException:
                logging.error(f'month {month[0:3]}-{year} was not found in selector')
                break

            try:
                # Obtain table with expenses
                month_expenses_table = self.driver.find_element(By.CLASS_NAME, 'tabla').text
                current_expenses = self.parse_and_filter_table(month_expenses_table) # Obtain table with expenses

                if current_expenses != None:
                    current_expenses['month'] = month_index + 1
                    current_expenses['year'] = year
                    expenses.append(current_expenses)
                    logger.info(f'expenses for {month[0:3]}-{year} were successfully parsed')

            except NoSuchElementException:
                logging.error(f'no data was found for {month[0:3]}-{year}')
                continue

            except Exception as e:
                logging.error(f'unexpected error parsing expenses for {month[0:3]}-{year}, error:\n{e}')
                continue

        self.expenses = expenses

    def parse_and_filter_table(self, html_table):
        pass

    def save_expenses(self):
        return NotImplementedError

    @property
    def expense_name():
        return NotImplementedError