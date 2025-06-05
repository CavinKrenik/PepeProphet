import os
from discord_webhook import DiscordWebhook

def send_discord_alert(message):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    DiscordWebhook(url=webhook_url, content=message).execute()