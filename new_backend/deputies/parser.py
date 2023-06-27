from bs4 import BeautifulSoup
from datetime import datetime
import requests

from deputies.profile import parse_deputy_profile
from deputies.expenses import (
    OfficesExpensesParser,
    OperationalExpensesParser,
    StaffExpensesParser,
)
from utils.drivers import get_driver
from utils.data import OPENDATA_CAMARA_URL, CURRENT_DEPUTIES_URL
from utils.db import (
    insert_deputy_profile,
    find_profile_data_in_db,
    insert_parlamentary_period,
    insert_operational_expenses,
    insert_office_expenses,
    insert_staff_expenses,
)

BASE_PROFILES_URL = 'https://www.camara.cl/diputados/detalle/biografia.aspx?prmId='
BASE_PROFILE_PIC_URL = 'https://www.camara.cl/img.aspx?prmID=GRCL'
BASE_DEPUTY_INFO_URL = OPENDATA_CAMARA_URL + 'WSDiputado.asmx/retornarDiputado?prmDiputadoId='


class DeputyParser:
    def __init__(self, index=0):
        self.local_index = index # Belongs to the interval [0, count_deputies-1]
        self.real_index = self.get_real_index()

        self.profile_html_url = BASE_PROFILES_URL + str(self.real_index)
        self.profile_pic_url = BASE_PROFILE_PIC_URL + str(self.real_index)
        self.deputy_info_url = BASE_DEPUTY_INFO_URL + str(self.real_index) 

        self.profile = None


    def get_real_index(self):
        """
        Given a local index between 0 and the total number of deputies, returns the id of a deputy.
        :return: Returns the id of the deputy, used in the deputies chamber.
        """
        response = requests.get(CURRENT_DEPUTIES_URL)
        soup = BeautifulSoup(response.content, 'xml')

        deputies = soup.find_all('Diputado')
        deputy = deputies[self.local_index]
        real_index = int(deputy.find('Id').get_text())
        return real_index


    def update_profile(self, save=True):
        """
        Method used to scrap information from the profile of a deputy, given a deputy id.
        :return: Returns basic information of the deputy.
        """

        self.profile = parse_deputy_profile(self.profile_html_url, self.deputy_info_url)
        self.profile['id'] = self.real_index
        self.profile['local_id'] = self.local_index
        self.profile['profile_picture'] = self.profile_pic_url
        self.profile['last_update'] = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        if save: # Save profile to database
            insert_deputy_profile(self.profile)
    
            # Update parlamentary periods
            for period in self.profile['periods']:
                period_from, period_to = period.split('-')
                insert_parlamentary_period({
                    'id': self.profile['id'],
                    'period_from': int(period_from),
                    'period_to': int(period_to),
                })

        return self.profile


    def load_or_update_profile(self):
        """
        Loads deputy profile data from database if it exists, otherwise updates it.
        """
        db_profile_data = find_profile_data_in_db(self.real_index)
        if db_profile_data:
            self.profile = db_profile_data
        else:
            update_profile()


    def update_deputy_expenses(self, save=True, driver=None):
        """
        Gets the expenses of a deputy in the last 5 months with records.
        :return: Returns a dictionary containing 
            - Operational expenses
            - Offices expenses
            - Staff expenses
        """
        print(f"(ID-{self.local_index}) Updating expenses of {self.profile['first_name']} {self.profile['first_surname']}, This may take few minutes...")
    
        op_exp = self.update_expenses_category(OperationalExpensesParser, driver=driver)
        if save: insert_operational_expenses(op_exp, self.real_index)

        of_exp = self.update_expenses_category(OfficesExpensesParser, driver=driver)
        if save: insert_office_expenses(of_exp, self.real_index)

        st_exp = self.update_expenses_category(StaffExpensesParser, driver=driver)
        if save: insert_staff_expenses(st_exp, self.real_index)

        print(f"(ID-{self.local_index}) Expenses of {self.profile['first_name']} {self.profile['first_surname']} successfully updated.")


    def update_expenses_category(self, expenses_parser, driver=None):
        """
        Gets the operational expenses of a deputy in the last 5 months with records.
        :return: Returns a dictionary containing the expenses of the deputy.
        """
        if not driver:
            driver = get_driver()

        expenses_parser = expenses_parser(self.profile, driver=driver)
        expenses_data = expenses_parser.get_deputy_expenses()
        return expenses_data



    # def get_attendance(self):
    #     """
    #     Method used to get the attendance of a deputy for all the chamber sessions of the
    #     current legislature.
    #     :return: Returns a dictionary containing the number of days attended, unattended justified or not, the total
    #     number of days and the official percentage of attended days.
    #     """
    #     # Measure elapsed time
    #     t_init = perf_counter()

    #     # Get attendance data
    #     attendance = parse_deputy_attendance(self.real_index)

    #     # Show summary
    #     print('[Attendance] Obtained')
    #     print('[Attendance] Elapsed time: ', round(perf_counter() - t_init, 3), 's', end='\n\n')

    #     return attendance


    # def get_last_votes(self):
    #     """
    #     Method used to get vote information from all voting of the last legislature,
    #     :return: Returns a list of dictionaries containing each one the name, description, date and the vote_option
    #              for a voting.
    #     """

    #     # Measure elapsed time
    #     t_init = perf_counter()

    #     # Get voting data
    #     voting = parse_deputy_votings(self.real_index, votes_limit=10)

    #     # Show summary
    #     print('[Voting] Obtained')
    #     print('[Voting] Elapsed time: ', round(perf_counter() - t_init, 3), 's', end='\n\n')

    #     return voting
