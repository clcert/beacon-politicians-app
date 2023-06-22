from bs4 import BeautifulSoup
import requests

from deputies.parsers.profile import parse_deputy_profile
from utils.data import OPENDATA_CAMARA_URL, CURRENT_DEPUTIES_URL

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

    def update_profile(self):
        """
        Method used to scrap information from the profile of a deputy, given a deputy id.
        :return: Returns basic information of the deputy.
        """

        profile = parse_deputy_profile(self.profile_html_url, self.deputy_info_url)
        profile['id'] = self.real_index
        profile['local_id'] = self.local_index
        profile['profile_picture'] = self.profile_pic_url

        # Show summary
        print(f"Main profile of {profile['first_name']} {profile['first_surname']} (ID-{self.local_index}) successfully updated.")

        return profile


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


    # def get_deputy_expenses(self):
    #     """
    #     Method used to get the expenses of a deputy for all the chamber sessions of the
    #     current legislature.
    #     :return: Returns a dictionary containing last 6 months deputy expenses.
    #     """
    #     json_data = get_json_data(json_file=JsonFiles.EXPENSES)

    #     average_expenses = json_data['average_expenses']
        
    #     expenses_data = json_data['expenses']
    #     deputy_data = expenses_data[self.local_index]

    #     deputy_operational_expenses = deputy_data['expenses']['operational']
    #     avg_operational_expenses_list = average_expenses['operational']

    #     for month_data in deputy_operational_expenses:
    #         avg_expenses_filtered_by_month = filter(
    #             lambda avg_data: avg_data['month'] == month_data['month'],
    #             avg_operational_expenses_list,
    #         )

    #         avg_expenses_month_list = list(avg_expenses_filtered_by_month)

    #         if not avg_expenses_month_list:
    #             # If there is no data for the month, set all values to -1
    #             for expense_category in OP_EXPENSES_TYPES:
    #                 month_data[expense_category] = {
    #                     'amount': -1,
    #                     'mean': -1,
    #                     'stdev': -1,
    #                 }
    #             continue

    #         avg_expenses_month = avg_expenses_month_list[0]
    #         avg_expenses_detail = avg_expenses_month['detail']

    #         for expense_category in OP_EXPENSES_TYPES:
    #             deputy_amount = month_data[expense_category]
    #             month_data[expense_category] = {
    #                 'amount': deputy_amount,
    #                 'mean': avg_expenses_detail[expense_category]['total'],
    #                 'stdev': avg_expenses_detail[expense_category]['total_std'],
    #             }

    #         month_data['mean'] = avg_expenses_month['total']
    #         month_data['stdev'] = avg_expenses_month['total_std']
        
    #     deputy_offices_expenses = deputy_data['expenses']['offices']
    #     avg_offices_expenses_list = average_expenses['offices']
    #     self._join_avg_expenses(deputy_offices_expenses, avg_offices_expenses_list)
        
    #     deputy_staff_expenses = deputy_data['expenses']['staff']
    #     avg_staff_expenses_list = average_expenses['staff']
    #     self._join_avg_expenses(deputy_staff_expenses, avg_staff_expenses_list)

    #     return deputy_data['expenses']


    # def _join_avg_expenses(self, expenses_data, avg_expenses_list):
    #     for month_data in expenses_data:
    #         avg_expenses_filtered_by_month = filter(
    #             lambda avg_data: avg_data['month'] == month_data['month'],
    #             avg_expenses_list,
    #         )

    #         avg_expenses_month_list = list(avg_expenses_filtered_by_month)
    #         if not avg_expenses_month_list:
    #             month_data['mean'] = -1
    #             month_data['stdev'] = -1
    #             continue

    #         avg_expenses_month = avg_expenses_month_list[0]
    #         month_data['mean'] = avg_expenses_month['total']
    #         month_data['stdev'] = avg_expenses_month['total_std']
