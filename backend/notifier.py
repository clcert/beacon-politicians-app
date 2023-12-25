from notifications.make_post import DeputiesPost
from random import seed, randint
from utils.db import find_deputy_for_date
from utils.settings import MONTHS
from utils.utils import get_number_of_deputies, get_today_timestamp, get_json_data
from notifications.diffusers import Notifier, TelegramDiffuser, DiscordDiffuser, TwitterDiffuser
from deputies.parser import DeputyParser

import requests

TELEGRAM_TOKEN = 'TELEGRAM_TOKEN'
TELEGRAM_CHAT_ID = 'TELEGRAM_CHAT_ID'
DISCORD_WEBHOOK_ID = 'DISCORD_WEBHOOK_ID'
TWITTER_CONSUMER_KEY = 'TWITTER_CONSUMER_KEY'
TWITTER_CONSUMER_SECRET = 'TWITTER_CONSUMER_SECRET'
TWITTER_ACCESS_TOKEN = 'TWITTER_ACCESS_TOKEN'
TWITTER_ACCESS_TOKEN_SECRET = 'TWITTER_ACCESS_TOKEN_SECRET'


def check_todays_deputy_in_db():
    """
    Checks if the deputy of the day is already saved in the database.
    """
    today = get_today_timestamp().strftime('%Y-%m-%d %H:%M:%S')
    return find_deputy_for_date(today)

def make_post(deputy, message_content):
    profile = deputy['profile']
    DeputiesPost(
        name=f"{profile['name']} {profile['firstSurname']}",
        date=message_content['date'],
        gender=profile["gender"],
        party=message_content['party'],
        district=f"Distrito {profile['district']}",
        picture_url=profile['picture'],
        communes=profile['communes'],
        attendance_percentage=message_content['attendance'],
        expenses=message_content['exp_operational'],
        ranking=message_content['exp_operational_ranking'],
        proposed_law_projects=deputy['activity']['all'],
        published_law_projects=deputy['activity']['published'],
        pulse=f"{deputy['beacon']['pulseId']}-{deputy['beacon']['chainId']}",
    ).generate_post()


def get_message_content_for_deputy(deputy):
    """
    Returns the message to be shared for the given deputy.
    """
    # Basic Info
    profile = deputy["profile"]
    deputy_name = "{} {} {}".format(
        profile["name"],
        profile["firstSurname"],
        profile["secondSurname"]
    )
    dep_pronoun = "El diputado" if profile["gender"] == "MALE" else "La diputada"
    political_party = profile["party"]

    # Attendance
    attendance = deputy["attendance"]
    attendance_percentage = 1 - (attendance["unjustifiedAbsent"] / attendance["total"])
    attendance_percentage = round(attendance_percentage * 100, 2)

    # Expenses
    expenses = deputy["expenses"]
    expenses.sort(key=lambda x: x["code"], reverse=True)
    expenses_last_month = expenses[0]

    # Operational Expenses
    operational_expenses = expenses_last_month["detail"][1]
    total_operational = operational_expenses["amount"]
    mean_operational = operational_expenses["deputiesAvg"]
    ranking_operational = operational_expenses["deputiesRanking"]
    operational_comment = "sobre" if total_operational > mean_operational else "bajo"

    # Staff Expenses
    staff_expenses = expenses_last_month["detail"][0]
    total_staff = staff_expenses["amount"]
    mean_staff = staff_expenses["deputiesAvg"]
    ranking_staff = staff_expenses["deputiesRanking"]
    staff_comment = "sobre" if total_staff and total_staff > mean_staff else "bajo"

    projects = deputy["activity"]
    projects_total = projects["all"]
    projects_published = projects["published"] if projects["published"] > 0 else "ninguno"
    
    published = "han sido publicados" if projects["published"] > 1 else "ha sido publicado"
    [_ , month, day] = deputy["date"].split('-')
    month = MONTHS[int(month) - 1]
    date_str = f'{day} de {month}'

    message_content = {
        "date": date_str,
        "name": deputy_name,
        "party": political_party,
        "pronoun": dep_pronoun,
        "twitter": profile["twitterUsername"],
        "attendance": attendance_percentage,
        "exp_operational": total_operational,
        "exp_support_staff": total_staff,
        "exp_operational_comment": operational_comment,
        "exp_support_staff_comment": staff_comment,
        "exp_operational_ranking": ranking_operational,
        "exp_support_staff_ranking": ranking_staff,
        "projects_total": projects_total,
        "projects_published": f"{projects_published} {published}",
    }

    return message_content

def checkout_deputy(success_notifier, failure_notifier):
    db_data = check_todays_deputy_in_db()
    if not db_data:
        failure_notifier.notify_error(
            'No se ha encontrado el diputado de hoy en la base de datos'
        )
        exit(1)

    (deputy_id, chain_id, pulse_id, randOut) = db_data
    response = requests.get(f'https://random.uchile.cl/beacon/2.1-beta/chain/{chain_id}/pulse/{pulse_id}').json()
    pulse = response['pulse']
    pulseRandOut = pulse['outputValue']

    if randOut != pulseRandOut:
        failure_notifier.notify_error(
            f'El pulso almacenado en la base de datos posee un valor de randOut ({randOut}) distinto al valor de randOut en el beacon ({pulseRandOut}).'
        )
        exit(1)

    seed(pulseRandOut)
    index = randint(0, get_number_of_deputies() - 1)
    parser = DeputyParser(index)

    if parser.real_index != deputy_id:
        failure_notifier.notify_error(
            f'El diputado de hoy es el {parser.real_index} y no el {deputy_id}, como se encuentra en la base de datos.'
        )
        exit(1)

    json_data = get_json_data()
    deputies = json_data['records']
    deputy = list(filter(lambda x: x['date'] == get_today_timestamp().strftime('%Y-%m-%d'), deputies))
    if not deputy:
        failure_notifier.notify_error(
            f'El diputado de hoy no se encuentra en el archivo JSON.'
        )
        exit(1)

    message_content_dict = get_message_content_for_deputy(deputy[0])
    make_post(deputy[0], message_content_dict)
    success_notifier.notify(message_content_dict)

if __name__ == '__main__':
    diffDc = DiscordDiffuser('DcBot', 'Diputados Bot', DISCORD_WEBHOOK_ID)
    diffTg = TelegramDiffuser('TgBot', TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
    diffTw = TwitterDiffuser('TwBt', TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    success_notifier = Notifier([diffDc, diffTg, diffTw])
    failure_notifier = Notifier([diffDc])
    checkout_deputy(success_notifier, failure_notifier)
