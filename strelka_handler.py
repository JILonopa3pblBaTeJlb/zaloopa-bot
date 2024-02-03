import random
from telegram import Update
from telegram.ext import CallbackContext
from config import STRELKA_REPLYS_LIST


def handle_strelka(update: Update, context: CallbackContext, user_id):
    chat_data = context.chat_data

    if chat_data.get('mode') != 'STRELKA':
        return False

    reply_to_message = update.message.reply_to_message
    if not reply_to_message or reply_to_message.from_user.id != context.bot.id:
        return False

    if user_id == chat_data['strelka_user']:
        update.message.reply_text(random.choice(STRELKA_REPLYS_LIST))
        chat_data['strelka_count'] = chat_data.get('strelka_count', 0) + 1
        if chat_data['strelka_count'] >= 3:
            chat_data['mode'] = 'NORMAL'
            chat_data['strelka_count'] = 0
        return True

    return False
