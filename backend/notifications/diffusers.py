from requests_oauthlib import OAuth1Session
import requests

class Diffuser:
    def __init__(self, name: str):
        self.name = name

    def format_msg(self, message: str):
        return message
    
    def format_error(self, message: str):
        return 'ERROR: ' + message

    def share(self, message: str):
        print(f"Sharing {message} through {self.name}.")
        raise NotImplementedError
    

class Notifier:
    def __init__(self, diffusers: list[Diffuser]):
        self.diffusers = diffusers

    def notify_error(self, message: str):
        print(f"ERROR: {message}")
        for diffuser in self.diffusers:
            try:
                diffuser.share(diffuser.format_error(message))
            except Exception:
                print(f"Error at {diffuser.name}")

    def notify(self, message: str):
        print(f"NOTIFY: {message}")
        for diffuser in self.diffusers:
            try:
                diffuser.share(diffuser.format_msg(message))
            except Exception:
                print(f"Error at {diffuser.name}")
    

class TelegramDiffuser(Diffuser):
    def __init__(self, name, token, chat_id):
        super().__init__(name)
        self.url = f'https://api.telegram.org/bot{token}/sendMessage'
        self.chat_id = chat_id

    def format_msg(self, message):
        message = message.replace('diputado del día', '*diputado del día*')
        message = message.replace('diputada del día', '*diputada del día*')
        message += '\nPara más información, puedes visitar la página diputado.labs.clcert.cl.'
        return message

    def share(self, message):
        data = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        requests.post(self.url, data=data)
    

class DiscordDiffuser(Diffuser):
    def __init__(self, name, bot_username, webhook_id):
        super().__init__(name)
        self.url = f'https://discord.com/api/webhooks/{webhook_id}'
        self.username = bot_username

    def format_msg(self, message):
        message = message.replace('diputado del día', '**diputado del día**')
        message = message.replace('diputada del día', '**diputada del día**')
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

    def format_msg(self, message):
        message = message.replace('diputado del día', '#DiputadoDelDía')
        message = message.replace('diputada del día', '#DiputadaDelDía')
        return message[:280]
    
    def share(self, message):
        # Make the request
        oauth = OAuth1Session(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.access_token,
            resource_owner_secret=self.access_token_secret,
        )

        payload = { "text": message }

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
        
        reply_payload = {
            "text": (
                "Para más información, puedes visitar la página diputado.labs.clcert.cl. " +
                "Utilizamos la aleatoriedad pública y verificable de #RandomUChile para elegir al (a la) #DiputadxDelDia. " +
                "Toda la información es obtenida desde la página oficial de la cámara de diputados 😉."
            ),
            "reply": {
                "in_reply_to_tweet_id": tweet_id
            }
        }
        # Making the second request
        response = oauth.post(
            "https://api.twitter.com/2/tweets",
            json=reply_payload,
        )

        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )
