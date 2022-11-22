from selenium import webdriver

from .offices import get_deputy_offices_expenses as get_offices_expenses
from .operational import get_deputy_operational_expenses as get_operational_expenses
from .staff import get_deputy_staff_expenses as get_staff_expenses

def get_deputy_expenses(profile):
    """
        Returns a dictionary with expenses related to a deputy
        in the current year, grouped by month.
    """
    options = webdriver.ChromeOptions()
    # Location of Google Chrome binary
    options.binary_location = '/opt/google/chrome/google-chrome'
    options.add_argument("--headless") # We don't need a GUI
    driver = webdriver.Chrome('chromedriver', options=options)

    operational_expenses = get_operational_expenses(profile['deputy_id'], driver)

    name_offices_expenses = f'{profile["first_surname"]} {profile["second_surname"][0]}., {profile["first_name"]}'
    offices_expenses = get_offices_expenses(name_offices_expenses, driver)

    name_staff_expenses = f'{profile["first_surname"]} {profile["second_surname"]}, {profile["first_name"]}'
    staff_expenses = get_staff_expenses(name_staff_expenses, driver)

    driver.close()

    return {
        'operational': operational_expenses,
        'offices': offices_expenses,
        'staff': staff_expenses
    }
