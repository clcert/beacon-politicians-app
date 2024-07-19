from datetime import datetime
from models.models import Deputy, DailyDeputy, get_engine
from utils.beacon import get_pulse_data, get_local_index
from utils.utils import get_midnight_timestamp
from utils.json_builder import generate_deputy_json_data
from utils.argparser import SelectorArgParser
from collectors.profile import ProfileCollector


def choose_deputy(date: datetime, from_db=True) -> None:
    """
    Chooses a random deputy using as seed the pulse of Random UChile
    associated to a given date.
    """
    midnight_datetime = get_midnight_timestamp(date)
    (chainId, pulseId, randOut) = get_pulse_data(midnight_datetime)
    local_index = get_local_index(randOut)
    local_index = 2

    if from_db:
        todays_deputy = Deputy.get_deputy_by_local_id(local_index)
        daily_deputy = DailyDeputy(
            deputy_id=todays_deputy.id,
            date=midnight_datetime.strftime('%Y-%m-%d'),
            chain_index=chainId,
            pulse_index=pulseId,
            pulse_value=randOut
        )
        daily_deputy.save_or_update(refresh=True)
        generate_deputy_json_data(daily_deputy)
    else: 
        pc = ProfileCollector(local_index)
        pc.get_profile()
        profile = pc.profile
        print(
            f"El diputado del día {midnight_datetime.strftime('%d/%m/%Y')} es: {profile['name']} {profile['father_surname']} {profile['mother_surname']}." + "\n" +
            f"Selección en base al pulso #{pulseId} de la cadena #{chainId}, desde el Faro de Aleatoriedad de Random UChile."
        )


if __name__ == '__main__':
    args = SelectorArgParser().parse_args()

    if args.date:
        datetime_obj = args.date
        if datetime_obj > datetime.today():
            print("Error La fecha ingresada debe ser mayor o igual a la fecha actual.")
            exit(1)
    else:
        datetime_obj = datetime.today()

    if args.load_from_db:
        choose_deputy(datetime_obj, from_db=True)
    else:
        choose_deputy(datetime_obj, from_db=False)