from collectors.expenses.expenses import ExpensesCollector
from collectors.access_points import CamaraCL
from models.models import SupportStaffExpense

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class StaffExpensesCollector(ExpensesCollector):
    def __init__(self, profile, **kwargs):
        super().__init__(**kwargs)
        self.deputy_name = f'{profile["father_surname"]} {profile["mother_surname"][0]}., {profile["name"]}'
        self.deputy_full_name = f'{profile["name"]} {profile["father_surname"]}, {profile["mother_surname"]}'
        self.deputy_id = profile['id']
        self.url = CamaraCL.staff_expenses
        self.month_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_ddlMes'
        self.year_selector_id = 'ContentPlaceHolder1_ContentPlaceHolder1_ddlAno'

    def parse_and_filter_table(self, html_table):
        lines = html_table.split('\n')
        total = 0
        staff_num = 0

        for line in lines[2:]:
            fields = line.split('   ')
            curr_dep_name = fields[0][2:].strip()
            if curr_dep_name == self.deputy_name or curr_dep_name == self.deputy_full_name:
                staff_num += 1
                if fields[1].strip() != '(*)' and fields[1].strip() != '(**)':
                    total += int(fields[3].strip().replace('.', ''))
                else:
                    total += int(fields[4].strip().replace('.', ''))

        return { 'num_personal': staff_num, 'total': total } if staff_num > 0 else None

    @property
    def expense_name(self):
        return 'staff'

    def save_expenses(self):
        for expense in self.expenses:
            SupportStaffExpense(
                deputy_id=self.deputy_id,
                year=expense['year'],
                month=expense['month'],
                hired_staff=expense['num_personal'],
                amount=expense['total']
            ).save_or_update()
        logger.info(f'staff expenses for deputy {self.deputy_id} were saved')