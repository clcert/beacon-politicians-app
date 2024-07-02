from collectors.profile import ProfileCollector
from collectors.expenses.operational import OperationalExpensesCollector
from collectors.expenses.staff import StaffExpensesCollector

DEPUTIES_NUM = 155

def update():
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

        break

if __name__ == '__main__':
    update()