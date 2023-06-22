from utils.custom_parser import CustomParser
from utils.db import init_db
from utils.actions import update_all_profiles, update_expenses

if __name__ == '__main__':
    args = CustomParser().parse_args()

    if args.init:
        init_db()
        
    if args.update_profiles:
        update_all_profiles()

    if args.update_expenses:
        update_expenses(
            from_id=args.update_expenses[0],
            to_id=args.update_expenses[1]
        )
