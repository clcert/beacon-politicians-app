from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from .offices import get_deputy_offices_expenses as get_offices_expenses
from .operational import get_deputy_operational_expenses as get_operational_expenses

def get_deputy_expenses(deputy_id, deputy_name):
    """
        Returns a dictionary with expenses related to a deputy
        in the current year, grouped by month.
    """
    print(deputy_name)
    options = webdriver.ChromeOptions()
    # Location of Google Chrome binary
    options.binary_location = '/opt/google/chrome/google-chrome'
    options.add_argument("--headless") # We don't need a GUI
    driver = webdriver.Chrome('chromedriver', options=options)

    offices_expenses = get_offices_expenses(deputy_name, driver)
    operational_expenses = get_operational_expenses(deputy_id, driver)

    driver.close()

    return {
        'offices': offices_expenses,
        'operational': operational_expenses,
    }
