from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

# TODO: Add support for multiple years
def get_deputy_operational_expenses(deputy_id, driver):
  """ Returns a dictionary with the expenses of a deputy in the current year """

  url = f'https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx?prmId={deputy_id}'
  month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes'
  driver.get(url)
  expenses = dict()
  for month in MONTHS:
    try:
      month_selector = Select(driver.find_element(By.ID, month_selector_id))
      month_selector.select_by_visible_text(month)
      sleep(1) # wait for page to load
      month_expenses_table = driver.find_element(By.XPATH, '//*[@class="tabla"]').text
      expenses[month] = parse_html_table(month_expenses_table)
      print(f'Got expenses for {month}')
    except Exception as e:
      print(f'Could not find expenses for {month}')

  return expenses

def parse_html_table(table):
  lines = table.splitlines()
  expenses = dict()
  for line in lines[1:]:
    [title, amount] = line.split('   ')
    expenses[title] = int(amount.strip().replace('.', ''))
  return expenses

def main(dep_id):
  options = webdriver.ChromeOptions()
  options.binary_location = '/opt/google/chrome/google-chrome'
  options.add_argument("--headless")
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
  expenses = get_deputy_operational_expenses(dep_id, driver)
  driver.close()
  return expenses


if __name__ == '__main__':
  main(74)