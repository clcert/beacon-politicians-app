from bs4 import BeautifulSoup
from datetime import datetime
import requests

from deputies.attendance import parse_deputy_attendance
from deputies.profile import parse_deputy_profile
from deputies.votings import parse_deputy_votings
from deputies.expenses import (
    OfficesExpensesParser,
    OperationalExpensesParser,
    StaffExpensesParser,
)
from deputies.activity import ActivityParser
from utils.drivers import get_driver
from utils.data import OPENDATA_CAMARA_URL, CURRENT_DEPUTIES_URL
from utils.db import (
    insert_deputy_profile,
    find_profile_data_in_db,
    get_real_index_from_db,
    insert_parlamentary_period,
    insert_operational_expenses,
    insert_office_expenses,
    insert_staff_expenses,
    insert_attendance_record,
    insert_voting_record,
    insert_law_project_record,
    insert_deputy_of_the_day,
    find_operational_expenses_for_deputy,
    find_staff_expenses_for_deputy,
    find_law_projects_for_deputy,
    find_deputy_periods,
    delete_previous_voting_records,
)

BASE_PROFILES_URL = 'https://www.camara.cl/diputados/detalle/biografia.aspx?prmId='
BASE_PROFILE_PIC_URL = 'https://www.camara.cl/img.aspx?prmID=GRCL'
BASE_DEPUTY_INFO_URL = OPENDATA_CAMARA_URL + 'WSDiputado.asmx/retornarDiputado?prmDiputadoId='


class DeputyParser:
    def __init__(self, index=0, chain_id=None, pulse_id=None, rand_out=None):
        self.local_index = index # Belongs to the interval [0, count_deputies-1]
        self.real_index = self.get_real_index()

        self.chain_id = chain_id
        self.pulse_id = pulse_id
        self.rand_out = rand_out

        self.profile_html_url = BASE_PROFILES_URL + str(self.real_index)
        self.profile_pic_url = BASE_PROFILE_PIC_URL + str(self.real_index)
        self.deputy_info_url = BASE_DEPUTY_INFO_URL + str(self.real_index) 

        self.profile = None


    def get_real_index(self):
        """
        Given a local index between 0 and the total number of deputies, returns the id of a deputy.
        :return: Returns the id of the deputy, used in the deputies chamber.
        """
        db_index = get_real_index_from_db(self.local_index)
        if db_index:
            return db_index
        else: 
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
            self.update_profile()
    

    def saved_deputy_expenses(self) -> bool:
        """
        Checks if the expenses of a deputy are already saved in the database.
        """
        self.op_exp = find_operational_expenses_for_deputy(self.real_index)
        self.st_exp = find_staff_expenses_for_deputy(self.real_index)
        return self.op_exp and self.st_exp
    

    def saved_legislative_activity(self) -> bool:
        """
        Checks if the activity of a deputy is already saved in the database.
        """
        self.law_projects = find_law_projects_for_deputy(self.real_index)
        return self.law_projects


    def update_deputy_expenses(self, save=True, driver=None):
        """
        Gets the expenses of a deputy in the last 5 months with records.
        :return: Returns a dictionary containing 
            - Operational expenses
            - Offices expenses
            - Staff expenses
        """
        print(f"[Parser] Updating expenses of {self.profile['first_name']} {self.profile['first_surname']} ({self.local_index+1}), this may take few minutes...")
    
        self.op_exp = self.update_expenses_category(OperationalExpensesParser, driver=driver)
        if save: insert_operational_expenses(self.op_exp, self.real_index)

        self.of_exp = self.update_expenses_category(OfficesExpensesParser, driver=driver)
        if save: insert_office_expenses(self.of_exp, self.real_index)

        self.st_exp = self.update_expenses_category(StaffExpensesParser, driver=driver)
        if save: insert_staff_expenses(self.st_exp, self.real_index)

        return {
            'operational_expenses': self.op_exp,
            'office_expenses': self.of_exp,
            'staff_expenses': self.st_exp,
        }
    

    def update_legislative_activity(self, save=True, driver=None):
        parser = ActivityParser(self.real_index, driver=driver)
        year_init_period = find_deputy_periods(self.real_index)[0][0]
        self.law_projects = parser.get_deputy_activity(from_date=datetime(year_init_period, 3, 10))
        if save:
            for law_project in self.law_projects:
                insert_law_project_record(law_project, self.real_index)
        return self.law_projects


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


    def update_attendance(self, save=True):
        """
        Method used to get the attendance of a deputy for all the chamber sessions of the
        current legislature.
        """
        self.attendance = parse_deputy_attendance(self.real_index)
        if save: 
            insert_attendance_record(self.attendance, self.real_index)

        return self.attendance


    def get_last_votes(self, save=True):
        """
        Method used to get vote information from all voting of the last legislature,
        :return: Returns a list of dictionaries containing each one the name, description, date and the vote_option
                 for a voting.
        """
        self.voting = parse_deputy_votings(self.real_index, votes_limit=20)
        if save:
            delete_previous_voting_records(self.real_index)
            for vote in self.voting:
                insert_voting_record(vote, self.real_index)

        return self.voting


    def save_as_deputy_of_the_day(self, timestamp):
        """
        Method used to save the deputy of the day in the database.
        """
        insert_deputy_of_the_day({
            "deputy_id": self.real_index,
            "chain_id": self.chain_id,
            "pulse_id": self.pulse_id,
            "rand_out": self.rand_out,
            "date": timestamp,
        })
