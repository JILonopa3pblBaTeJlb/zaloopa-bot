import random
from telegram import Update
from telegram.ext import CallbackContext
from anekdot import get_anekdot
from reduplication_handler import reduplicate
from gpt_handler import get_gpt_response

def ejikificate(update: Update, context: CallbackContext):
    ejikificated_message = f"{update.message.text} лол ок"
    update.message.reply_text(ejikificated_message)

def garipotterize(update: Update, context: CallbackContext):
    garipotterized_message = "гарри поттер и " + ' '.join(update.message.text.split()[:3])
    update.message.reply_text(garipotterized_message)

def osleficate(update: Update, context: CallbackContext):
    osleficated_message = ' '.join(update.message.text.split()[:2]) + " у тебя в жопе"
    update.message.reply_text(osleficated_message)

def send_anekdot(update: Update, context: CallbackContext):
    update.message.reply_text(get_anekdot())

def handle_sanya_for_random(update: Update, context: CallbackContext):
    gpt_response = get_gpt_response(update.message.text, update, context)
    update.message.reply_text(gpt_response)

def random_reply(update: Update, context: CallbackContext):
    functions = [reduplicate, garipotterize, osleficate, send_anekdot, ejikificate, handle_sanya_for_random]
    probabilities = [0.3, 0.05, 0.2, 0.3, 0.05, 0.1]
    random.choices(functions, weights=probabilities, k=1)[0](update, context)
