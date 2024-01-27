import time
from telegram import Update
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    chat_data = context.chat_data
    chat_data['debil_mode'] = True
    chat_data['mode'] = 'NORMAL'
    chat_data['dialogue_count'] = 0
    chat_data['strelka_count'] = 0
    context.bot.send_message(chat_id=update.effective_chat.id, text="ухбл ебать")

def restart(update: Update, context: CallbackContext):
    chat_data = context.chat_data
    chat_data['debil_mode'] = True
    chat_data['mode'] = 'NORMAL'
    chat_data['dialogue_count'] = 0
    chat_data['strelka_count'] = 0
    context.bot.send_message(chat_id=update.effective_chat.id, text="ух бля ебать два раза")

def brain(update: Update, context: CallbackContext):
    try:
        with open('prompt.txt', 'r') as file:
            content = file.read()
            update.message.reply_text(content)
    except FileNotFoundError:
        update.message.reply_text("Файл prompt.txt не найден.")
    except Exception as e:
        update.message.reply_text(f"Произошла ошибка: {e}")

def brainedit(update: Update, context: CallbackContext):
    new_prompt = ' '.join(context.args)
    with open('prompt.txt', 'w') as file:
        file.write(new_prompt)
    update.message.reply_text("Моск олександра перепрошит")

def diag(update: Update, context: CallbackContext):
    chat_data = context.chat_data
    mode = chat_data.get('mode', 'ХЗ')
    dialogue_count = chat_data.get('dialogue_count', 0)
    strelka_count = chat_data.get('strelka_count', 0)
    debil_mode_status = 'включен' if context.bot_data.get('debil_mode') else 'отключен'
    current_time = time.time()
    last_gpt_response_time = context.bot_data.get('last_gpt_response_time', None)
    time_since_last_gpt = current_time - last_gpt_response_time if last_gpt_response_time is not None else None
    diag_message = (
        f"Текущий режим: {mode}\n"
        f"Счетчик диалога: {dialogue_count}\n"
        f"Счетчик 'Стрелка': {strelka_count}\n"
        f"Режим долбоеба: {debil_mode_status}\n"
    )
    diag_message += f"обезьяний моск работал последний раз назад {time_since_last_gpt:.2f} секунд\n" if time_since_last_gpt is not None else "обезьяний моск еще не включали.\n"
    update.message.reply_text(diag_message)

def debil(update: Update, context: CallbackContext):
    debil_mode = context.bot_data.get('debil_mode', False)
    context.bot_data['debil_mode'] = not debil_mode
    update.message.reply_text("Режим долбоеба отключен." if debil_mode else "Режим долбоеба включен.")
