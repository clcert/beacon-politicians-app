from updater import collect_deputy_info
from datetime import datetime, timedelta
from sys import argv

days_to_calculate = int(argv[1]) if len(argv) > 1 else 1
days_to_calculate = min(days_to_calculate, 7)

dt_utc = datetime.utcnow()
dt_local = datetime.now()

consider_today = dt_utc.day > dt_local.day or (
    dt_utc.day == dt_local.day and dt_utc.hour > 3
)

if consider_today:
    initial_date = (datetime.now() - timedelta(days=days_to_calculate-1))
else:
    initial_date = (datetime.now() - timedelta(days=days_to_calculate))

initial_date = initial_date.replace(hour=0, minute=0, second=0, microsecond=0)

# Populates the json with the last 7 days
for delta in range(days_to_calculate):
    date = (initial_date + timedelta(days=delta))
    collect_deputy_info(timestamp=date)