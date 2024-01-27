import random
from telegram import Update
from telegram.ext import CallbackContext

STRELKA_REPLYS_LIST = [
    "то чо борзый дохуя самый", "слышь охуел ты ли чо?", "ебать ты дерзота",
    "втащу тебе чо скажешь тогда", "ты ща в рог словиш э", "ты предъявить решил или чо я не вкурю",
    "слышь рамс попутал кучерявый я эбал завязывай моросить", "чорт я тя найду",
    "попутавший ты ли чо", "э бля нахуй фильтруй базар", "слышь ты реально выхватишь сейчас"
]

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
