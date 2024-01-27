import random
import re
from telegram import Update
from telegram.ext import CallbackContext
from special_events import special_events
from random_replies import random_reply
from anekdot import get_anekdot
from reduplication_handler import reduplicate
from dialogue_handler import handle_dialogue, DIALOGUE_LIST
from strelka_handler import handle_strelka, STRELKA_REPLYS_LIST
from debil_mode import handle_debil_mode  # Импортируйте handle_debil_mode

def contains_cyrillic(text):
    """Проверяет, содержит ли текст кириллические символы."""
    return bool(re.search('[а-яА-Я]', text))

def handle_message(update: Update, context: CallbackContext):
    if not update.message:
        return

    chat_data = context.chat_data
    user_id = update.message.from_user.id
    reply_to_message = update.message.reply_to_message
    text = update.message.text.lower()
    special_event_reply = special_events(update, context)

    # Обработка специальных событий в любом режиме
    if special_event_reply:
        update.message.reply_text(special_event_reply)
        return

    # Проверка на реплай
    if reply_to_message and reply_to_message.from_user.id == context.bot.id:
        if chat_data.get('mode') != 'STRELKA':
            chat_data['mode'] = 'DIALOGUE'
        chat_data['dialogue_count'] = chat_data.get('dialogue_count', 0) + 1

        # Переключение в режим 'STRELKA'
        if chat_data.get('mode') == 'DIALOGUE':
            if chat_data['dialogue_count'] >= 3:
                chat_data['mode'] = 'STRELKA'
                chat_data['strelka_count'] = 0
                chat_data['dialogue_count'] = 0
                response = random.choice(STRELKA_REPLYS_LIST)
            else:
                response = random.choice(DIALOGUE_LIST)

            # Применение handle_debil_mode к тексту ответа, если debil_mode включен
            if context.bot_data.get('debil_mode', False):
                response = handle_debil_mode(response, context)
            
            update.message.reply_text(response)
            return

        # Обработка режима 'STRELKA'
        elif chat_data.get('mode') == 'STRELKA':
            chat_data['strelka_count'] += 1
            if chat_data['strelka_count'] >= 3:
                chat_data['mode'] = 'NORMAL'
                chat_data['strelka_count'] = 0
                chat_data['dialogue_count'] = 0
            else:
                response = random.choice(STRELKA_REPLYS_LIST)
                # Применение handle_debil_mode к тексту ответа, если debil_mode включен
                if context.bot_data.get('debil_mode', False):
                    response = handle_debil_mode(response, context)

                update.message.reply_text(response)
            return

    # Обработка режима 'NORMAL' и случайных ответов
    if random.random() <= 0.1: 
        random_reply(update, context)
