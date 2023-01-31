from updater import Updater
from datetime import datetime, timedelta
from sys import argv

updater = Updater()

days = int(argv[1]) if len(argv) > 1 else 1
days -= 1

# Populates the json with the last 7 days
for delta in range(days,-1,-1):
    date = (datetime.now() - timedelta(days=delta)).replace(hour=0, minute=0, second=0, microsecond=0)
    print(date)
    updater.update(using_json=True, date_hour=date)