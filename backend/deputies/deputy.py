from bs4 import BeautifulSoup
from time import perf_counter
from datetime import datetime

import requests

# parsers
from deputies.parsers.profile import parse_deputy_profile
from deputies.parsers.attendances import parse_deputy_attendance
from deputies.parsers.votings import parse_deputy_votings
from deputies.parsers.expenses import (
    OfficesExpensesParser,
    OperationalExpensesParser,
    StaffExpensesParser
)

# settings
from settings import (
    BASE_PROFILES_URL,
    BASE_PROFILE_PIC_URL,
    BASE_DEPUTY_INFO_URL,
    CURRENT_DEPUTIES_URL,
)


class DeputyParser:
    def __init__(self, index=0):
        self.local_index = index # Belongs to the interval [0, count_deputies-1]
        self.real_index = self.get_real_index()

        self.profile_html_url = BASE_PROFILES_URL + str(self.real_index)
        self.profile_pic_url = BASE_PROFILE_PIC_URL + str(self.real_index)
        self.deputy_info_url = BASE_DEPUTY_INFO_URL + str(self.real_index) 

        self.profile = None

    def get_data(self):
        """
        Method used to get all information related to a deputy.
        :return: Returns a dictionary containing all deputy's information.
        """
        print(f'Date: {datetime.today()}')
        print('Loading new deputy...', end='\n\n')

        self.profile = self.get_profile()
        self.profile['attendance'] = self.get_attendance()
        self.profile['voting'] = self.get_last_votes()
        self.profile['expenses'] = self.get_deputy_expenses()

        return self.profile

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

    def get_profile(self):
        """
        Method used to scrap information from the profile of a deputy, given a deputy id.
        :return: Returns basic information of the deputy.
        """
        # Measure elapsed time
        t_init = perf_counter()

        profile = parse_deputy_profile(self.profile_html_url, self.deputy_info_url)
        profile['photo'] = self.profile_pic_url
        profile['termination'] = 'o' if profile['sex'] == '1' else 'a'
        profile['treatment'] = 'Sr' if profile['sex'] == '1' else 'Sra'
        profile['deputy_id'] = self.real_index

        # Show summary
        print('[Main Profile] Obtained')
        print('[Main Profile] Deputy: ', profile['first_name'], profile['first_surname'])
        print('[Main Profile] Elapsed time: ', round(perf_counter() - t_init, 3), 's', end='\n\n')

        return profile


    def get_attendance(self):
        """
        Method used to get the attendance of a deputy for all the chamber sessions of the
        current legislature.
        :return: Returns a dictionary containing the number of days attended, unattended justified or not, the total
        number of days and the official percentage of attended days.
        """
        # Measure elapsed time
        t_init = perf_counter()

        # Get attendance data
        attendance = parse_deputy_attendance(self.real_index)

        # Show summary
        print('[Attendance] Obtained')
        print('[Attendance] Elapsed time: ', round(perf_counter() - t_init, 3), 's', end='\n\n')

        return attendance


    def get_last_votes(self):
        """
        Method used to get vote information from all voting of the last legislature,
        :return: Returns a list of dictionaries containing each one the name, description, date and the vote_option
                 for a voting.
        """

        # Measure elapsed time
        t_init = perf_counter()

        # Get voting data
        voting = parse_deputy_votings(self.real_index, votes_limit=10)

        # Show summary
        print('[Voting] Obtained')
        print('[Voting] Elapsed time: ', round(perf_counter() - t_init, 3), 's', end='\n\n')

        return voting

    def get_deputy_expenses(self):
        """
        Method used to get the expenses of a deputy for all the chamber sessions of the
        current legislature.
        :return: Returns a dictionary containing the number of days attended, unattended justified or not, the total
        number of days and the official percentage of attended days.
        """
        # Measure elapsed time
        t_init = perf_counter()

        parsers = {
            'operational': OperationalExpensesParser,
            'offices': OfficesExpensesParser,
            'staff': StaffExpensesParser,
        }

        all_expenses = {}

        for expense_name, parser in parsers.items():
            current_parser = parser(self.profile)
            expenses_data = current_parser.get_deputy_expenses()
            if expenses_data == []:
                print(f'[Expenses] {expense_name.capitalize()} Not found.')
            else:
                print(f'[Expenses] {expense_name.capitalize()} Obtained.')
            all_expenses[expense_name] = expenses_data

        # Show summary
        print('[Expenses] Obtained')
        print('[Expenses] Elapsed time: ', round(perf_counter() - t_init, 3), 's', end='\n\n')
        
        return all_expenses