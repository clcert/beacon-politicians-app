from datetime import datetime
from random import seed, randint
from utils.db import find_deputy_for_date
from utils.data import MONTHS
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

def get_message_for_deputy(deputy):
    """
    Returns the message to be shared for the given deputy.
    """
    profile = deputy["profile"]
    deputy_name = f'{profile["name"]} {profile["first_surname"]} {profile["second_surname"]}'
    dep_pronoun = "El diputado" if profile["gender"] == "MALE" else "La diputada"
    political_party = profile["party_alias"]

    attendance = deputy["attendance"]
    attendance_percentage = round((attendance["attended"] + attendance["justified_absent"]) / attendance["total"] * 100, 2)

    expenses = deputy["expenses"]
    expenses.sort(key=lambda x: x["code"], reverse=True)
    expenses_last_month = expenses[0]
    total_amount = expenses_last_month["total"]

    average_month_amount = 0
    ignore_keys = ["total", "month", "year", "code"]
    for (key, value) in expenses_last_month.items():
        if key not in ignore_keys:
            cat_avg = value["deputies_avg"] if value["deputies_avg"] else 0
            average_month_amount += cat_avg
    amount_comment = "sobre" if total_amount > average_month_amount else "bajo"

    projects = deputy["activity"]
    projects_total = projects["all"]
    projects_published = projects["published"] if projects["published"] > 0 else "ninguno"
    
    published = "han sido publicados" if projects["published"] > 1 else "ha sido publicado"
    [_ , month, day] = deputy["date"].split('-')
    month = MONTHS[int(month) - 1]
    date_str = f'{day} de {month}'

    msg = (
        f"{dep_pronoun} del día {date_str} es {deputy_name} ({political_party}). " +
        f"Su porcentaje de asistencia es del {attendance_percentage}%. " +
        f"En el último mes con registro gastó ${total_amount:,} ".replace(',','.') +
        f"({amount_comment} el promedio de la Cámara). " +
        f"Ha presentado {projects_total} proyectos de ley, de los cuales {projects_published} {published}."
    )
    return msg

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
    deputy = list(filter(lambda x: x['index'] == deputy_id, deputies))
    if not deputy:
        failure_notifier.notify_error(
            f'El diputado de hoy no se encuentra en el archivo JSON.'
        )
        exit(1)
    
    message = get_message_for_deputy(deputy[0])
    success_notifier.notify(message)

if __name__ == '__main__':
    diffDc = DiscordDiffuser('DcBot', 'Diputados Bot', DISCORD_WEBHOOK_ID)
    diffTg = TelegramDiffuser('TgBot', TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
    diffTw = TwitterDiffuser('TwBt', TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
    success_notifier = Notifier([diffDc, diffTg, diffTw])
    failure_notifier = Notifier([diffDc])
    checkout_deputy(success_notifier, failure_notifier)
