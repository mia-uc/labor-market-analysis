import urllib
import requests
from dotenv import load_dotenv
import os
import traceback

load_dotenv()


class NotifierBot:
    def __init__(self) -> None:
        self._token = os.getenv("TELEGRAM_NOTIFIER_BOT_TOKE")

        assert self._token

    def push(self, chat, message):
        assert chat

        url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (
            self._token, chat, urllib.parse.quote_plus(message))

        _ = requests.get(url)

    def error(self, chat, session):
        tb_info = traceback.format_exc()

        return self.push(chat, f'{session} has been stopped because\n\n{tb_info}')
