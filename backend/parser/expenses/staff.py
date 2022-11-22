from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep

MONTHS = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']

def get_deputy_staff_expenses(deputy_name, driver):
	""" 
		Returns a dictionary with expenses related to office of a deputy
		in the current year, grouped by month.
	"""
	print(deputy_name)
	# Page with Offices Expenses data
	url = f'https://www.camara.cl/transparencia/personalapoyogral.aspx'
	month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_ddlMes'
	driver.get(url)
	staff_expenses = dict()
	for month in MONTHS:
		try:
			# Change the month in form
			month_selector = Select(driver.find_element(By.ID, month_selector_id))
			month_selector.select_by_visible_text(month) # Set corresponding month
			sleep(1) # wait for page to load
			month_expenses_table = driver.find_element(By.XPATH, '//*[@id="tabla"]').text
			# Obtain the expenses and filter by deputy
			month_expenses = parse_and_filter_table(month_expenses_table, deputy_name)
			if month_expenses != []:
				staff_expenses[month] = month_expenses
		except Exception as e:
			continue

	return staff_expenses

def parse_and_filter_table(table, deputy_name):
	lines = table.splitlines()
	staff = []
	for line in lines[2:]:
		fields = line.split('   ')
		curr_dep_name = fields[0][2:].strip()
		if curr_dep_name == deputy_name:
			staff.append({
				'position': fields[1].strip(),
				'amount': int(fields[2].strip().replace('.', '')),
			})
	return staff

if __name__ == '__main__':
	options = webdriver.ChromeOptions()
	# Location of Goofle Chrome binary
	options.binary_location = '/opt/google/chrome/google-chrome'
	options.add_argument("--headless") # We don't need a GUI
	driver = webdriver.Chrome('chromedriver', options=options)

	# Using the driver we obtain the expenses
	expenses = get_deputy_staff_expenses('Naranjo Ortiz, Jaime', driver)
	driver.close()