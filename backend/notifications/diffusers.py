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
        # for diffuser in self.diffusers:
        #     diffuser.share(diffuser.format_error(message))

    def notify(self, message: str):
        print(f"NOTIFY: {message}")
        for diffuser in self.diffusers:
            diffuser.share(diffuser.format_msg(message))
    

class TelegramDiffuser(Diffuser):
    def __init__(self, name, token, chat_id):
        super().__init__(name)
        self.url = f'https://api.telegram.org/bot{token}/sendMessage'
        self.chat_id = chat_id

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
        message.replace('diputado del día', '#DiputadoDelDía')
        message.replace('diputada del día', '#DiputadaDelDía')
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
            "text": "Toda esta información y más la puedes encontrar en diputado.labs.clcert.cl.\nInformación obtenida desde www.camara.cl",
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
