import requests
from settings import TOKEN_TELEGRAM_BOT, TELEGRAM_CHAT_ID

def send_notification(message):
    """
    Sends a telegram alert with the given message.
    :param message: message to send.
    :return:
    """
    url = f'https://api.telegram.org/bot{TOKEN_TELEGRAM_BOT}/sendMessage'
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    requests.post(url, data=data)


def format_success_message(profile):
    """
    Formats a message to send to telegram.
    :param profile: profile to format.
    :return: formatted message.
    """
    message = f"*{profile['first_name']} {profile['first_surname']}* es "
    message += "el diputado " if profile['sex'] == '1' else "la diputada "
    message += f"del día {profile['date'].split(' ')[0]}!"

    message += "\n\n"
    message += f"Su porcentaje de asistencia es de *{profile['attendance']['percentage']}%* dentro de la presente legislatura."
    
    operational_expenses = [exp['total'] for exp in profile['expenses']['operational']]
    mean_operational_expenses = sum(operational_expenses) / len(operational_expenses) if len(operational_expenses) > 0 else 0

    offices_expenses = [exp['total'] for exp in profile['expenses']['offices']]
    mean_offices_expenses = sum(offices_expenses) / len(offices_expenses) if len(offices_expenses) > 0 else 0

    staff_expenses = [exp['total'] for exp in profile['expenses']['staff']]
    mean_staff_expenses = sum(staff_expenses) / len(staff_expenses) if len(staff_expenses) > 0 else 0

    message += "\n\n"
    message += "Su gasto promedio mensual se distribuye como sigue:\n"
    message += f"- Gastos Operacionales: *${mean_operational_expenses:,.0f}*\n".replace(',','.')
    message += f"- Gasto en Oficinas: *${mean_offices_expenses:,.0f}*\n".replace(',','.')
    message += f"- Gasto en Personal de Apoyo: *${mean_staff_expenses:,.0f}*\n".replace(',','.')
    message += f"Formando un total de de *${(mean_operational_expenses + mean_offices_expenses + mean_staff_expenses):,.0f}*.".replace(',','.')
    
    message += "\n\n"
    message += "Para ver más detalles, visita el siguiente enlace: "
    message += f"https://diputado.labs.clcert.cl"

    return message