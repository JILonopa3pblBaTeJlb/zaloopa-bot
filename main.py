from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from message_handler import handle_message
from command_handlers import start, restart, diag, brain, brainedittrololo, debil
from roll_handler import roll
from config import TOKEN

def send_error_to_user(update, context):
    msg = update.message
    if msg:
        msg.reply_text(f'товарищ сталин произошла чудовищная ошибка: {context.error}')
    else:
        print(f'Ошибка: {context.error}')

def error(update, context):
    send_error_to_user(update, context)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.bot_data['debil_mode'] = True

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("restart", restart))
    dp.add_handler(CommandHandler("roll", roll))
    dp.add_handler(CommandHandler("diag", diag))
    dp.add_handler(CommandHandler("brain", brain))
    dp.add_handler(CommandHandler("brainedittrololo", brainedittrololo))
    dp.add_handler(CommandHandler("debil", debil))
    
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
