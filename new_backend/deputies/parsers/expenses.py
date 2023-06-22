from time import sleep

# Selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from settings import (
    MONTHS,
    OP_EXPENSES_OFFICE,
    OP_EXPENSES_OTHERS,
    OP_EXPENSES_WEB,
)
from deputies.utils import get_current_month, get_current_year

class ExpensesParser:

    def __init__(self, driver=None):        
        self.driver = driver
        self.url = ''
        self.month_selector_id = ''


    def get_deputy_expenses(self):
        # Get the expenses page
        self.driver.get(self.url)
        expenses = []
        change_year = False

        # Get the current month and year
        month_index = get_current_month()
        year = get_current_year()
        
        while len(expenses) < 6:
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
                    year_selector.select_by_visible_text(str(year)) # Set corresponding year
                    change_year = False
                    sleep(1) # wait for page to load

                # Change month in form
                month_selector = Select(self.driver.find_element(By.ID, self.month_selector_id))
                month_selector.select_by_visible_text(month) # Set corresponding month

                sleep(1) # wait for page to load

                # Obtain table with expenses
                month_expenses_table = self.driver.find_element(By.XPATH, '//*[@class="tabla"]').text
                current_expenses = self.parse_and_filter_table(month_expenses_table) # Obtain table with expenses

                if current_expenses != None:
                    current_expenses['month'] = month
                    current_expenses['year'] = year
                    expenses.append(current_expenses)

            except Exception as e:
                # print('Error parsing expenses for month: ' + month + ' and year: ' + str(year))
                continue

        return expenses

    def parse_and_filter_table(self, html_table):
        pass


class OperationalExpensesParser(ExpensesParser):

    def __init__(self, profile, **kwargs):
        super().__init__(**kwargs)
        deputy_id = profile['deputy_id']
        self.url = f'https://www.camara.cl/diputados/detalle/gastosoperacionales.aspx?prmId={deputy_id}'
        self.month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlMes'
        self.year_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_DetallePlaceHolder_ddlAno'

    def parse_and_filter_table(self, html_table):
        lines = html_table.splitlines()
        expenses = dict()
        expenses['Otros gastos de oficina parlamentaria'] = 0
        expenses['Web y Almacenamiento'] = 0
        expenses['Otros'] = 0
        total = 0
        for line in lines[1:]:
            [title, amount] = line.split('   ')
            title = title.replace('(**monto ajustado por nota de crédito recibida)','').strip()
            integer_amount = int(amount.strip().replace('.', ''))
            total += integer_amount
            if title in OP_EXPENSES_OFFICE:
                expenses['Otros gastos de oficina parlamentaria'] += integer_amount
            elif title in OP_EXPENSES_WEB:
                expenses['Web y Almacenamiento'] += integer_amount
            elif title in OP_EXPENSES_OTHERS:
                expenses['Otros'] += integer_amount
            else:
                expenses[title.lower().capitalize()] = integer_amount
        expenses['total'] = total
        return expenses


class OfficesExpensesParser(ExpensesParser):

    def __init__(self, profile, **kwargs):
        super().__init__(**kwargs)
        self.deputy_name = f'{profile["first_surname"]} {profile["second_surname"][0]}., {profile["first_name"]}'
        self.url = 'https://www.camara.cl/transparencia/oficinasparlamentarias.aspx'
        self.month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_ddlMes'
        self.year_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_ddlAno'

    def parse_and_filter_table(self, html_table):
        lines = html_table.splitlines()
        total = 0
        num_offices = 0

        for line in lines[1:]:
            [city, region, amount, deputy] = line.split('   ')
            if deputy.strip() == self.deputy_name:
                num_offices += 1
                total += int(amount.strip().replace('.', ''))

        return { 'num_oficinas': num_offices, 'total': total } if num_offices > 0 else None


class StaffExpensesParser(ExpensesParser):

    def __init__(self, profile, **kwargs):
        super().__init__(**kwargs)
        self.deputy_name = f'{profile["first_surname"]} {profile["second_surname"]}, {profile["first_name"]}'
        self.url = 'https://www.camara.cl/transparencia/personalapoyogral.aspx'
        self.month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_ddlMes'
        self.year_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_ddlAno'

    def parse_and_filter_table(self, html_table):
        lines = html_table.splitlines()
        total = 0
        staff_num = 0

        for line in lines[2:]:
            fields = line.split('   ')
            curr_dep_name = fields[0][2:].strip()
            if curr_dep_name == self.deputy_name:
                staff_num += 1
                if fields[1].strip() != '(*)' and fields[1].strip() != '(**)':
                    total += int(fields[3].strip().replace('.', ''))
                else:
                    total += int(fields[4].strip().replace('.', ''))

        return { 'num_personal': staff_num, 'total': total } if staff_num > 0 else None
