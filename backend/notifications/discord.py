from discord import SyncWebhook
from settings import DISCORD_WEBHOOK_URL

def send_notification(message):
    webhook = SyncWebhook.from_url(DISCORD_WEBHOOK_URL)
    webhook.send(message)
