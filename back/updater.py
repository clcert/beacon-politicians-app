from collectors.profile import ProfileCollector
from collectors.expenses.operational import OperationalExpensesCollector
from collectors.expenses.staff import StaffExpensesCollector
from collectors.activity import ActivityCollector
from models.models import init_db
from utils.utils import DEPUTIES_NUM

from datetime import datetime


def update():
    init_db()
    for local_index in range(DEPUTIES_NUM):
        prof_col = ProfileCollector(local_index)
        prof_col.get_profile()
        prof_col.save_profile()

        exp_col = OperationalExpensesCollector(prof_col.profile)
        exp_col.get_deputy_expenses()
        exp_col.close_driver()
        exp_col.save_expenses()

        stf_col = StaffExpensesCollector(prof_col.profile)
        stf_col.get_deputy_expenses()
        stf_col.close_driver()
        stf_col.save_expenses()

        last_period = prof_col.periods[-1]
        year_init_period = last_period['start_date']
        deputy_id = prof_col.profile['id']
        act_col = ActivityCollector(deputy_id)
        act_col.get_deputy_activity(from_date=datetime(year_init_period, 3, 10))
        act_col.save_activity()

if __name__ == '__main__':
    update()