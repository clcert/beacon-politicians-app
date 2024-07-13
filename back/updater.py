from collectors.profile import ProfileCollector
from collectors.expenses.operational import OperationalExpensesCollector
from collectors.expenses.staff import StaffExpensesCollector
from collectors.activity import ActivityCollector
from collectors.attendance import AttendanceCollector
from collectors.voting import VotingCollector
from models.models import init_db, Deputy
from utils.drivers import get_driver
from utils.argparser import UpdaterArgParser

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def update_deputy_profile(local_index):
    prof_col = ProfileCollector(local_index)
    prof_col.get_profile()
    prof_col.save_profile()

    deputy_id = prof_col.profile['id']
    return deputy_id

def update_deputy_expenses(deputy_id, driver):
    exp_col = OperationalExpensesCollector(deputy_id, driver=driver)
    exp_col.get_deputy_expenses()
    exp_col.save_expenses()

    stf_col = StaffExpensesCollector(deputy_id, driver=driver)
    stf_col.get_deputy_expenses()
    stf_col.save_expenses()

def update_deputy_activity(deputy_id, driver):
    act_col = ActivityCollector(deputy_id, driver=driver)
    act_col.get_deputy_activity()
    act_col.save_activity()

def update_deputy_attendance(deputy_id):
    att_col = AttendanceCollector(deputy_id)
    att_col.get_attendance()
    att_col.save_attendance()

def update_deputy_votings(deputy_id):
    vot_col = VotingCollector(deputy_id)
    vot_col.get_votings(votes_limit=20)
    vot_col.save_votings()

def update(deputies_range, update_profile, update_activity, update_attendance, update_votings, update_expenses):
    init_db()

    driver = get_driver() if update_expenses or update_activity else None

    for local_index in deputies_range:
        if update_profile:
            logging.info(f"Actualizando el perfil del diputado {local_index}")
            deputy_id = update_deputy_profile(local_index)
        else:
            logging.info(f"Obteniendo el id real del diputado {local_index}")
            try:
                deputy_id = Deputy.get_deputy_by_local_id(local_index).id
            except AttributeError:
                logging.error(f"El diputado {local_index} no existe en la base de datos.")
                continue
        
        if update_activity:
            update_deputy_activity(deputy_id, driver)

        if update_expenses:
            update_deputy_expenses(deputy_id, driver)
        
        if update_attendance:
            update_deputy_attendance(deputy_id)

        if update_votings:
            update_deputy_votings(deputy_id)

    if driver:
        driver.quit()


if __name__ == '__main__':
    parser = UpdaterArgParser()
    args = parser.parse_args()
    
    if args.deputies_range:
        deputies_range = list(range(args.deputies_range[0], args.deputies_range[1] + 1))
    elif args.deputy_index:
        deputies_range = [args.deputy_index]
    else:
        exit("Por favor, especifique el rango de diputados a actualizar. Para más información, ejecute el comando con la opción -h.")
    
    update(
        deputies_range = deputies_range,
        update_profile = args.update_profile,
        update_activity = args.update_activity,
        update_attendance = args.update_attendance,
        update_votings = args.update_votings,
        update_expenses = args.update_expenses
    )