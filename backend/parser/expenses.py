from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

class ExpensesParser:

  def __init__(self):
    options = webdriver.ChromeOptions()
    # Location of Goofle Chrome binary
    options.binary_location = '/opt/google/chrome/google-chrome'
    options.add_argument("--headless") # We don't need a GUI
    driver = webdriver.Chrome('chromedriver', options=options)
    self.driver = driver
    self.url = ''
    self.month_selector_id = ''


  # TODO: Add support for multiple years
  def get_deputy_expenses(self):
    # Get the expenses page
    self.driver.get(self.url)
    expenses = dict()
    for month in MONTHS:
      try:
        # Change the month in form
        month_selector = Select(self.driver.find_element(By.ID, self.month_selector_id))
        month_selector.select_by_visible_text(month) # Set corresponding month
        sleep(1) # wait for page to load
        # Obtain table with expenses
        month_expenses_table = self.driver.find_element(By.XPATH, '//*[@class="tabla"]').text
        current_expenses = self.parse_and_filter_table(month_expenses_table) # Obtain table with expenses
        if current_expenses != None:
          expenses[month] = current_expenses
      except Exception as e:
        continue

    return expenses

  def parse_and_filter_table(self, html_table):
    pass

  def close_driver(self):
    self.driver.close()


class OperationalExpensesParser(ExpensesParser):

  def __init__(self, profile):
    super().__init__()
    deputy_id = profile['deputy_id']
    self.url = f'https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx?prmId={deputy_id}'
    self.month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes'

  def parse_and_filter_table(self, html_table):
    lines = html_table.splitlines()
    expenses = dict()
    for line in lines[1:]:
      [title, amount] = line.split('   ')
      expenses[title] = int(amount.strip().replace('.', ''))
    return expenses


class OfficesExpensesParser(ExpensesParser):

  def __init__(self, profile):
    super().__init__()
    self.deputy_name = f'{profile["first_surname"]} {profile["second_surname"][0]}., {profile["first_name"]}'
    self.url = 'https://www.camara.cl/transparencia/oficinasparlamentarias.aspx'
    self.month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_ddlMes'

  def parse_and_filter_table(self, html_table):
    lines = html_table.splitlines()
    offices = []
    for line in lines[1:]:
      [city, region, amount, deputy] = line.split('   ')
      if deputy.strip() == self.deputy_name:
        offices.append({
          'city': city.strip(),
          'region': region.strip(),
          'amount': int(amount.strip().replace('.', '')),
        })
    return offices if len(offices) > 0 else None


class StaffExpensesParser(ExpensesParser):

  def __init__(self, profile):
    super().__init__()
    self.deputy_name = f'{profile["first_surname"]} {profile["second_surname"]}, {profile["first_name"]}'
    self.url = 'https://www.camara.cl/transparencia/personalapoyogral.aspx'
    self.month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_ddlMes'

  def parse_and_filter_table(self, html_table):
    lines = html_table.splitlines()
    staff = []
    for line in lines[2:]:
      fields = line.split('   ')
      curr_dep_name = fields[0][2:].strip()
      if curr_dep_name == self.deputy_name:
        staff.append({
          'job': fields[2].strip(),
          'amount': int(fields[3].strip().replace('.', '')),
        })
    return staff if len(staff) > 0 else None
