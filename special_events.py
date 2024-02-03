import random
import re
from telegram import Update
from telegram.ext import CallbackContext
from anekdot import get_anekdot
from harrypotterturbo import harrypotterturbo
from strelka_handler import STRELKA_REPLYS_LIST
from gpt_handler import get_gpt_response
from norma import handle_norma
from config import SPECIAL_EVENTS_LIST, STRELKA_TRIGGERS_LIST


def special_events(update: Update, context: CallbackContext):
    message_text = update.message.text.lower()
    chat_data = context.chat_data

    for trigger in STRELKA_TRIGGERS_LIST:
        if trigger in message_text:
            chat_data['mode'] = 'STRELKA'
            chat_data['strelka_user'] = update.message.from_user.id
            chat_data['strelka_count'] = 0
            return random.choice(STRELKA_REPLYS_LIST)

    for word, reply_set in SPECIAL_EVENTS_LIST.items():
        if re.search(r'\b' + re.escape(word.lower()) + r'\b', message_text) or re.search(r'\b' + re.escape(word) + r'\b', message_text):
            if reply_set == "handle_sanya":
                return handle_sanya(word, message_text, update, context)
            elif reply_set == "handle_norma":
                return handle_norma(update, context)
            elif reply_set == "handle_ya_by":
                return handle_ya_by(message_text)
            elif reply_set in ["get_anekdot", "harrypotterturbo"]:
                return globals()[reply_set]()
            return random.choice(reply_set) if isinstance(reply_set, list) else reply_set
    return None


def handle_ya_by(message_text: str):
    ya_by_index = message_text.find(" я бы ")
    return f"ты бы и коня {message_text[ya_by_index + len(' я бы '):]}" if ya_by_index != -1 else None

def handle_sanya(key_word, message_text, update: Update, context: CallbackContext):
    prompt_part = message_text.split(key_word, 1)[1].strip() if key_word in message_text else ""
    return get_gpt_response(prompt_part, update, context)


