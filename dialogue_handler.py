from telegram import Update
from telegram.ext import CallbackContext
import random
from debil_mode import handle_debil_mode 
from config import DIALOGUE_LIST


def handle_dialogue(update: Update, context: CallbackContext):
    chat_data = context.chat_data
    chat_data['dialogue_count'] = chat_data.get('dialogue_count', 0) + 1
    dialogue_limit = 5

    if chat_data['dialogue_count'] >= dialogue_limit:
        chat_data['mode'] = 'NORMAL'
        chat_data['dialogue_count'] = 0
    else:
        update.message.reply_text(random.choice(DIALOGUE_LIST))
