from utils.custom_parser import CustomParser
from utils.db import init_db, create_db
from utils.actions import update_all_profiles, update_expenses, choose_deputy
from utils.utils import (
    get_datetime_from_epoch,
    get_datetime_from_date_and_time,
    get_today_timestamp,
)

if __name__ == '__main__':
    args = CustomParser().parse_args()

    if args.create_db:
        create_db()

    if args.init:
        init_db()
        
    if args.update_profiles:
        update_all_profiles()

    if args.expenses_activity_update:
        update_expenses(
            from_id=args.expenses_activity_update[0],
            to_id=args.expenses_activity_update[1]
        )

    if args.verify or args.run:
        if args.epoch:
            timestamp = get_datetime_from_epoch(args.epoch)
        elif args.date:
            timestamp = get_datetime_from_date_and_time(args.date, args.time)
        else: # If no arguments are given, use today at 00:00 hrs.
            timestamp = get_today_timestamp()
        
        choose_deputy(timestamp=timestamp, verify=args.verify)