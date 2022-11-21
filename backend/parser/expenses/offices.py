from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

def get_deputy_offices_expenses(deputy_name, driver):
	""" 
		Returns a dictionary with expenses related to office of a deputy
		in the current year, grouped by month.
	"""
	# Page with Offices Expenses data
	url = f'https://www.camara.cl/transparencia/oficinasparlamentarias.aspx'
	month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_ddlMes'
	driver.get(url)
	office_expenses = dict()
	for month in MONTHS:
		try:
			# Change the month in form
			month_selector = Select(driver.find_element(By.ID, month_selector_id))
			month_selector.select_by_visible_text(month) # Set corresponding month
			sleep(1) # wait for page to load
			month_expenses_table = driver.find_element(By.XPATH, '//*[@class="tabla"]').text
			# Obtain the expenses and filter by deputy
			month_expenses = list(
				filter(lambda x: x['deputy'] == deputy_name, parse_html_table(month_expenses_table))
			)
			if month_expenses != []:
				office_expenses[month] = list(map(lambda x: x.pop('deputy'), month_expenses))
				print(f'Got expenses for {month}')
			else:
				print(f'Could not find expenses for {month}')
		except Exception as e:
			print(f'Could not find expenses for {month}')

	return office_expenses

def parse_html_table(table):
	lines = table.splitlines()
	offices = []
	for line in lines[1:]:
		[city, region, amount, deputy] = line.split('   ')
		offices.append({
			'deputy': deputy.strip(),
			'city': city.strip(),
			'region': region.strip(),
			'amount': int(amount.strip().replace('.', '')),
		})
	return offices

def main(dep_name):
	options = webdriver.ChromeOptions()
	# Location of Goofle Chrome binary
	options.binary_location = '/opt/google/chrome/google-chrome'
	options.add_argument("--headless") # We don't need a GUI
	driver = webdriver.Chrome('chromedriver', options=options)

	# Using the driver we obtain the expenses
	expenses = get_deputy_offices_expenses(dep_name, driver)
	driver.close()
	return expenses


if __name__ == '__main__':
	main('Naranjo O., Jaime')