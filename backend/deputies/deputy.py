from bs4 import BeautifulSoup
from time import perf_counter
from datetime import datetime

import requests

# parsers
from deputies.parsers.profile import parse_deputy_profile
from deputies.parsers.attendances import parse_deputy_attendance
from deputies.parsers.votings import parse_deputy_votings

# utils
from deputies.utils import get_json_data

# settings
from settings import (
    BASE_PROFILES_URL,
    BASE_PROFILE_PIC_URL,
    BASE_DEPUTY_INFO_URL,
    CURRENT_DEPUTIES_URL,
    OP_EXPENSES_TYPES,
    JsonFiles,
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
        :return: Returns a dictionary containing last 6 months deputy expenses.
        """
        json_data = get_json_data(json_file=JsonFiles.EXPENSES)

        average_expenses = json_data['average_expenses']
        
        expenses_data = json_data['expenses']
        deputy_data = expenses_data[self.local_index]

        operational_expenses = deputy_data['expenses']['operational']
        avg_expenses_list = average_expenses['operational']
        for month_data in operational_expenses:
            avg_expenses_month = next(
                filter(
                    lambda avg_data: avg_data['month'] == month_data['month'],
                    avg_expenses_list,
                )
            )['detail']
            for expense_category in OP_EXPENSES_TYPES:
                deputy_amount = month_data[expense_category]
                month_data[expense_category] = {
                    'amount': deputy_amount,
                    'mean': avg_expenses_month[expense_category]['total'],
                    'stdev': avg_expenses_month[expense_category]['total_std'],
                }
        
        offices_expenses = deputy_data['expenses']['offices']
        avg_expenses_list = average_expenses['offices']
        for month_data in offices_expenses:
            avg_expenses_month = next(
                filter(
                    lambda avg_data: avg_data['month'] == month_data['month'],
                    avg_expenses_list,
                )
            )
            month_data['mean'] = avg_expenses_month['total']
            month_data['stdev'] = avg_expenses_month['total_std']
        
        staff_expenses = deputy_data['expenses']['staff']
        avg_expenses_list = average_expenses['staff']
        for month_data in staff_expenses:
            avg_expenses_month = next(
                filter(
                    lambda avg_data: avg_data['month'] == month_data['month'],
                    avg_expenses_list,
                )
            )
            month_data['mean'] = avg_expenses_month['total']
            month_data['stdev'] = avg_expenses_month['total_std']

        return deputy_data['expenses']
