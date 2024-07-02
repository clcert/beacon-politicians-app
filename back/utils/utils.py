from datetime import datetime
from pytz import timezone, UTC


DEPUTIES_NUM = 155

MONTHS = [
    "enero",    "febrero",  "marzo",        "abril",    "mayo",         "junio", 
    "julio",    "agosto",   "septiembre",   "octubre",  "noviembre",    "diciembre",
]

def get_current_month():
    return datetime.now().month

def get_current_year():
    return datetime.now().year

def get_midnight_timestamp(date: datetime) -> datetime:
    return datetime(year=date.year, month=date.month, day=date.day, hour=get_hrs_diff(), minute=0)

def get_hrs_diff():
    """
    Gets the difference between the chilean time and the UTC time.
    :return: Returns the difference in hours as an integer.
    """
    dt_utc = datetime.now(tz=UTC)
    dt_local = datetime.now(timezone("America/Santiago"))

    return (dt_utc.hour - dt_local.hour) % 24