import random
from telegram import Update
from telegram.ext import CallbackContext


def handle_norma(update: Update, context: CallbackContext):
    chat_data = context.chat_data
    sent_fragments = chat_data.get('sent_fragments', set())
    fragment_length = 450  

    try:
        with open('norma.txt', 'r', encoding='utf-8') as file:
            content = file.read()

        
        if len(sent_fragments) * fragment_length >= len(content):
            update.message.reply_text("норм у тебя в жопе")
            sent_fragments.clear()  

        while True:
            start_index = random.randint(0, len(content) - fragment_length)
            fragment = content[start_index:start_index + fragment_length]

            if start_index not in sent_fragments:
                sent_fragments.add(start_index)
                chat_data['sent_fragments'] = sent_fragments  
                update.message.reply_text(fragment)
                break

    except FileNotFoundError:
        update.message.reply_text("Файл norma.txt не найден.")
    except Exception as e:
        update.message.reply_text(f"Произошла ошибка: {e}")
