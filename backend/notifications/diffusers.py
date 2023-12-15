from requests_oauthlib import OAuth1Session
from io import BytesIO
import requests

class Diffuser:
    def __init__(self, name: str):
        self.name = name

    def format_msg(self, message_content_dict: dict):
        date_str = message_content_dict['date']
        deputy_name = message_content_dict['name']
        political_party = message_content_dict['party']
        dep_pronoun = message_content_dict['pronoun']
        attendance_percentage = message_content_dict['attendance']
        total_operational = message_content_dict['exp_operational']
        operational_comment = message_content_dict['exp_operational_comment']
        ranking_operational = message_content_dict['exp_operational_ranking']
        projects_total = message_content_dict['projects_total']
        projects_published = message_content_dict['projects_published']

        msg = (
            f"[MENSAJE DE PRUEBA] {dep_pronoun} del día {date_str} es {deputy_name} ({political_party}). \n\n" +
            f"Cuenta con un porcentaje de asistencia del {attendance_percentage}% "+
            f"en el presente período legislativo. \n\n" +
            f"En el último mes con información, destinó la suma de " +
            f"${total_operational:,} ".replace(',','.') +
            f"a gastos operacionales, monto que se encuentra {operational_comment} el promedio "+
            f"respecto a los demás diputados en la Cámara, ocupando así el puesto {ranking_operational} de 155 " +
            f"en el ranking de los diputados con mayores gastos. \n\n" +
            f"{dep_pronoun} ha presentado {projects_total} proyectos de ley, "+
            f"de los cuales {projects_published}."
        )
        return msg
    
    def format_error(self, message: str):
        return 'ERROR: ' + message

    def share(self, message: str):
        print(f"Sharing {message} through {self.name}.")
        raise NotImplementedError
    

class Notifier:
    def __init__(self, diffusers: "list[Diffuser]"):
        self.diffusers = diffusers

    def notify_error(self, message: str):
        print(f"ERROR: {message}")
        for diffuser in self.diffusers:
            try:
                diffuser.share(diffuser.format_error(message))
            except Exception:
                print(f"Error at {diffuser.name}")

    def notify(self, message_content_dict: dict):
        print(f"NOTIFYING")
        for diffuser in self.diffusers:
            try:
                message = diffuser.format_msg(message_content_dict)
                diffuser.share(message)
            except Exception as e:
                print(e)
                print(f"Error at {diffuser.name}")
    

class TelegramDiffuser(Diffuser):
    def __init__(self, name, token, chat_id):
        super().__init__(name)
        self.url = f'https://api.telegram.org/bot{token}/sendPhoto'
        self.chat_id = chat_id

    def format_msg(self, message_content_dict: dict):
        message = super().format_msg(message_content_dict)
        message = message.replace('diputada del día', '*diputada del día*')
        message = message.replace('diputado del día', '*diputado del día*')
        message += '\nPara más información, puedes visitar la página diputado.labs.clcert.cl.'
        return message

    def share(self, message):
        dep_pic = open('./todays_deputy.png', 'rb')
        pic = BytesIO(dep_pic.read())
        data = {
            'chat_id': self.chat_id,
            'caption': message,
            'parse_mode': 'Markdown',
        }
        media = {
            'photo': pic
        }
        requests.post(self.url, data=data, files=media)    

class DiscordDiffuser(Diffuser):
    def __init__(self, name, bot_username, webhook_id):
        super().__init__(name)
        self.url = f'https://discord.com/api/webhooks/{webhook_id}'
        self.username = bot_username

    def format_msg(self, message_content_dict: dict):
        message = super().format_msg(message_content_dict)
        message = message.replace('diputada del día', '**diputada del día**')
        message = message.replace('diputado del día', '**diputado del día**')
        message += '\nPara más información, puedes visitar la página https://diputado.labs.clcert.cl.'
        return message

    def share(self, message):
        data = {
            'content': message,
            'username': self.username
        }
        requests.post(self.url, data=data)


class TwitterDiffuser(Diffuser):
    def __init__(self, name, consumer_key, consumer_secret, access_token, access_token_secret):
        super().__init__(name)
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        
    def format_msg(self, message_content_dict: dict):
        """Twitter has its own message format."""
        date_str = message_content_dict['date']
        deputy_name = message_content_dict['name']
        twitter = message_content_dict['twitter']
        political_party = message_content_dict['party']
        dep_pronoun = message_content_dict['pronoun']
        attendance_percentage = message_content_dict['attendance']
        total_operational = message_content_dict['exp_operational']
        operational_comment = message_content_dict['exp_operational_comment']
        ranking_operational = message_content_dict['exp_operational_ranking']
        projects_total = message_content_dict['projects_total']
        projects_published = message_content_dict['projects_published']

        twitter_message = f"(@{twitter})" if twitter else ""

        message_1 = (
            f"{dep_pronoun} del día {date_str} es {deputy_name} {twitter_message} de {political_party}, " +
            f"quien cuenta con un porcentaje de asistencia del {attendance_percentage}% " +
            f"en el presente período legislativo. (1/4)"
        )
        message_1 = message_1.replace('diputado del día', '#DiputadoDelDía')
        message_1 = message_1.replace('diputada del día', '#DiputadaDelDía')

        message_2 = (
            f"En el último mes con información, {dep_pronoun.lower()} {deputy_name} destinó la suma de " +
            f"${total_operational:,} ".replace(',','.') +
            f"a gastos operacionales, ocupando así el puesto {ranking_operational} de 155 " +
            f"en el ranking de los diputados con mayores gastos ({operational_comment} el promedio de la Cámara). (2/4)"
        )

        message_3 = (
            f"{dep_pronoun} {deputy_name.split(' ')[1]} ha presentado {projects_total} proyectos de ley, "+
            f"de los cuales {projects_published}. (3/4)"
        )

        message_4 = (
            f"Para más información, puedes visitar nuestra página diputado.labs.clcert.cl. " +
            f"Utilizamos la aleatoriedad pública y verificable de #RandomUChile para elegir al (a la) #DiputadxDelDia. " +
            f"Toda la información es obtenida desde la página oficial de la cámara de diputados 😉. (4/4)"
        )

        entire_message = "\n\n\n".join([message_1, message_2, message_3, message_4])
        return entire_message
    
    def share(self, message):
        # Make the request
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )

        messages = message.split("\n\n\n")
        payload = { "text": "[TEST] "+messages[0] }

        # Making the request
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json=payload,
        )

        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )
        json_response = response.json()
        tweet_id = json_response['data']['id']

        # Publish replies
        for message in messages[1:]:
            reply_payload = {
                "text": "[TEST] "+message,
                "reply": {
                    "in_reply_to_tweet_id": tweet_id
                }
            }
            # Making the request
            response = oauth.post(
                "https://api.twitter.com/2/tweets",
                json=reply_payload,
            )

            if response.status_code != 201:
                raise Exception(
                    "Request returned an error: {} {}".format(response.status_code, response.text)
                )
            json_response = response.json()
            tweet_id = json_response['data']['id']
