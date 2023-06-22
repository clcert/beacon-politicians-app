from utils.custom_parser import CustomParser
from utils.db import init_db
from utils.updater import update_all_profiles

if __name__ == '__main__':
    args = CustomParser().parse_args()

    if args.init:
        init_db()
        
    if args.all_profiles:
        update_all_profiles()
