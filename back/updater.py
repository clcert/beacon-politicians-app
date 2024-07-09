from collectors.profile import ProfileCollector
from collectors.expenses.operational import OperationalExpensesCollector
from collectors.expenses.staff import StaffExpensesCollector
from collectors.activity import ActivityCollector
from collectors.attendance import AttendanceCollector
from collectors.voting import VotingCollector
from models.models import init_db
from utils.utils import DEPUTIES_NUM
from utils.drivers import get_driver

from datetime import datetime


def update():
    init_db()
    #driver = get_driver()
    #for local_index in range(DEPUTIES_NUM):
    prof_col = ProfileCollector(12)
    prof_col.get_profile()
    prof_col.save_profile()

    deputy_id = prof_col.profile['id']

    att_col = AttendanceCollector(deputy_id)
    att_col.get_attendance()
    att_col.save_attendance()

    vot_col = VotingCollector(deputy_id)
    vot_col.get_votings()
    vot_col.save_votings()


        # exp_col = OperationalExpensesCollector(prof_col.profile)
        # exp_col.get_deputy_expenses()
        # exp_col.close_driver()
        # exp_col.save_expenses()

        # stf_col = StaffExpensesCollector(prof_col.profile)
        # stf_col.get_deputy_expenses()
        # stf_col.close_driver()
        # stf_col.save_expenses()

        # last_period = prof_col.periods[-1]
        # year_init_period = last_period['start_date']
        # deputy_id = prof_col.profile['id']
        # act_col = ActivityCollector(deputy_id, driver=driver)
        # act_col.get_deputy_activity(from_date=datetime(year_init_period, 3, 10))
        # act_col.save_activity()
    # driver.quit()

if __name__ == '__main__':
    update()