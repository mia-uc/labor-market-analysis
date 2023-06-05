
from telebot import types
import random
import telebot
from dotenv import load_dotenv
import os
import logging
from db.python_mongo_tools import MongoInterfaces
import re

logging.basicConfig(
    format='[%(levelname)s][%(asctime)s]: %(message)s',
    level=logging.INFO
)
log = logging.getLogger(__name__)


load_dotenv()

INIT_MESSAGE = """\
Hi‼️ I'm @Job_Coach_Bot.

I can help you find a job.
Everyday, I find and save a lot of jobs from various job boards. 

I recommend that you subscribe 🔔 to your most frequent searches to keep you updated on 🆕 offers that match your search. 

However, you can ask me any time and I will list the main job offers for that simple search.
"""

SEARCH_LABEL = """Ok 😆, but, remember if you are pretty interested \
in the query that you will do is better to subscribe it.

Anyhow, Tell me what's your query 🤔""",


def generate_buttons(bts_names, markup):
    for button in bts_names:
        markup.add(types.KeyboardButton(button))
    return markup


def run():
    db = MongoInterfaces("Users")

    TOKEN = os.getenv("TELEGRAM_NOTIFIER_BOT_TOKE")
    bot = telebot.TeleBot(TOKEN)
    log.info(f"Bot Init {TOKEN}")

    options = ['Subscribe 👀', 'Search 🔎']

    def send_hello(message):
        log.info(f'Init Conversation with {message.chat.id}')
        user = db.exists(id=message.chat.id)
        if not user:
            # {message.chat
            #   'id': ******,
            #   'type': 'private',
            #   'title': None,
            #   'username': 'DanielOOP',
            #   'first_name': 'DanielOOP',
            #   'last_name': None,
            #   'is_forum': None,
            #   'photo': None,
            #   'bio': None,
            #   'join_to_send_messages': None,
            #   'join_by_request': None,
            #   'has_private_forwards': None,
            #   'has_restricted_voice_and_video_messages': None,
            #   'description': None,
            #   'invite_link': None,
            #   'pinned_message': None,
            #   'permissions': None,
            #   'slow_mode_delay': None,
            #   'message_auto_delete_time': None,
            #   'has_protected_content': None,
            #   'sticker_set_name': None,
            #   'can_set_sticker_set': None,
            #   'linked_chat_id': None,
            #   'location': None,
            #   'active_usernames': None,
            #   'emoji_status_custom_emoji_id': None,
            #   'has_hidden_members': None,
            #   'has_aggressive_anti_spam_enabled': None
            # }

            user = db.insert({
                'id': message.chat.id,
                'username': message.chat.username,
                'first_name': message.chat.first_name,
                'subscriptions': []
            })

            log.info(f'{message.chat.id} was created')

        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup = generate_buttons(options, markup)
        message = bot.reply_to(message, INIT_MESSAGE, reply_markup=markup)

    @bot.message_handler()
    def multiplexer(message):
        if message.text == '/start':
            send_hello(message)
        elif message.text.startswith('/'):
            find_one(message)

        elif message.text == 'Subscribe 👀':
            message = bot.reply_to(
                message,
                "Great 🤩, Tell me what query you want me to keep you updated on",
            )

            bot.register_next_step_handler(message, add_subscription)

        elif message.text == 'Search 🔎':
            message = bot.reply_to(message, SEARCH_LABEL)
            bot.register_next_step_handler(message, search_handler)
        else:
            markup = types.ReplyKeyboardMarkup(row_width=2)
            markup = generate_buttons(options, markup)
            message = bot.reply_to(
                message,
                "If you want to find some jobs, first, choose an option ",
                reply_markup=markup
            )
            bot.register_next_step_handler(message, multiplexer)

    def add_subscription(message):
        user = db.exists(id=message.chat.id)
        user['subscriptions'].append(message.text)

        db.update(
            {'subscriptions': user['subscriptions']},
            id=message.chat.id
        )

        bot.reply_to(
            message,
            f"Perfect, You were subscribed to the query {message.text}",
        )

        search_handler(message)

    def _search_handler(query, skip):
        def f(message):
            if message.text == 'Show me more 🧐':
                search_handler(message, query, skip)
            else:
                multiplexer(message)
        return f

    def search_handler(message, query=None, skip=0):
        if query:
            jobs = [
                {'name': "la tiza en vinagre by query", 'id': 84593},
                {'name': "la tiza en vinagre by query", 'id': 84593},
                {'name': "la tiza en vinagre by query", 'id': 84593},
                {'name': "la tiza en vinagre by query", 'id': 84593},
                {'name': "la tiza en vinagre by query", 'id': 84593},
            ]
        else:
            jobs = [{'name': "la tiza en vinagre", 'id': 84593}]

        # db.search(message.text, only_new=False)

        answer = f"These are the main offers for that \n"
        for j in jobs:
            answer += f"\n/{j['id']} - {j['name']}"

        markup = types.ReplyKeyboardMarkup(row_width=2)
        markup = generate_buttons(['Show me more 🧐'], markup)
        message = bot.reply_to(message, answer, reply_markup=markup)

        bot.register_next_step_handler(message, _search_handler(
            query if not query is None else message.text,
            skip=skip + 10
        ))

    def find_one(message):
        job = {'sms': "hola"}
        message = bot.reply_to(message, job['sms'])

    # Launches the bot in infinite loop mode with additional
    # ...exception handling, which allows the bot
    # ...to work even in case of errors.
    bot.infinity_polling()
