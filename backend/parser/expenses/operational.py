from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

# TODO: Add support for multiple years
def get_deputy_operational_expenses(deputy_id, driver):
  """ Returns a dictionary with the expenses of a deputy in the current year """
  # Page with Operational Expenses data
  url = f'https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx?prmId={deputy_id}'
  month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes'
  driver.get(url)
  expenses = dict()
  for month in MONTHS:
    try:
      # Change the month in form
      month_selector = Select(driver.find_element(By.ID, month_selector_id))
      month_selector.select_by_visible_text(month) # Set corresponding month
      sleep(1) # wait for page to load
      month_expenses_table = driver.find_element(By.XPATH, '//*[@class="tabla"]').text
      expenses[month] = parse_html_table(month_expenses_table) # Obtain table with expenses
    except Exception as e:
      continue

  return expenses

def parse_html_table(table):
  lines = table.splitlines()
  expenses = dict()
  for line in lines[1:]:
    [title, amount] = line.split('   ')
    expenses[title] = int(amount.strip().replace('.', ''))
  return expenses

if __name__ == '__main__':
  options = webdriver.ChromeOptions()
  # Location of Goofle Chrome binary
  options.binary_location = '/opt/google/chrome/google-chrome'
  options.add_argument("--headless") # We don't need a GUI
  driver = webdriver.Chrome('chromedriver', options=options)

  # Using the driver we obtain the expenses
  expenses = get_deputy_operational_expenses(74, driver)
  driver.close()