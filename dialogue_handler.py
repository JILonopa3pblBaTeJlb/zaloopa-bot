from telegram import Update
from telegram.ext import CallbackContext
import random
from debil_mode import handle_debil_mode 

DIALOGUE_LIST = [
    "ну а дальше что", "и что дальше", "нет, ты объясни", "но почему", "а это почему",
    "а почему это", "ага и чо дальше", "это ты так думаешь", "поясни", "я не понял, чо еще раз?",
    "и что", "повтори", "в смысле", "а чо в смысле", "чо еще ляпнешь", "сам додумался?",
    "чо ты хочешь-то?", "чо сказал щас", "а по фактам?", "мне показалось или ты быканул?",
    "это зачем щас сказал", "ты кто такой", "ты где есть то", "конкретнее", "подробнее",
    "обоснуй", "и чо к чему", "а ну повтори"
]

def handle_dialogue(update: Update, context: CallbackContext):
    chat_data = context.chat_data
    chat_data['dialogue_count'] = chat_data.get('dialogue_count', 0) + 1
    dialogue_limit = 5

    if chat_data['dialogue_count'] >= dialogue_limit:
        chat_data['mode'] = 'NORMAL'
        chat_data['dialogue_count'] = 0
    else:
        update.message.reply_text(random.choice(DIALOGUE_LIST))
