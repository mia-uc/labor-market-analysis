import urllib
import requests
from dotenv import load_dotenv
import os

load_dotenv()


class NotifierBot:
    def __init__(self) -> None:
        self._token = os.getenv("TELEGRAM_NOTIFIER_BOT_TOKE")

    def push(self, chat, message):
        url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (
            self.token, chat, urllib.parse.quote_plus(message))

        _ = requests.get(url)
