import random
import re
from telegram import Update
from telegram.ext import CallbackContext
from special_events import special_events
from random_replies import random_reply
from dialogue_handler import DIALOGUE_LIST
from strelka_handler import STRELKA_REPLYS_LIST

def contains_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def handle_message(update: Update, context: CallbackContext):
    if not update.message:
        return

    chat_data = context.chat_data
    user_id = update.message.from_user.id
    reply_to_message = update.message.reply_to_message
    text = update.message.text.lower()
    special_event_reply = special_events(update, context)

    if special_event_reply:
        update.message.reply_text(special_event_reply)
        return

    if reply_to_message and reply_to_message.from_user.id == context.bot.id:
        if chat_data.get('mode') != 'STRELKA':
            chat_data['mode'] = 'DIALOGUE'
        chat_data['dialogue_count'] = chat_data.get('dialogue_count', 0) + 1

        if chat_data.get('mode') == 'DIALOGUE':
            if chat_data['dialogue_count'] >= 3:
                chat_data['mode'] = 'STRELKA'
                chat_data['strelka_count'] = 0
                chat_data['dialogue_count'] = 0
                update.message.reply_text(random.choice(STRELKA_REPLYS_LIST))
                return
            update.message.reply_text(random.choice(DIALOGUE_LIST))
            return

        if chat_data.get('mode') == 'STRELKA':
            chat_data['strelka_count'] += 1
            if chat_data['strelka_count'] >= 3:
                chat_data['mode'] = 'NORMAL'
                chat_data['strelka_count'] = 0
                chat_data['dialogue_count'] = 0
            else:
                update.message.reply_text(random.choice(STRELKA_REPLYS_LIST))
            return

    if random.random() <= 0.1: 
        random_reply(update, context)
