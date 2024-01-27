import random
import re
from telegram import Update
from telegram.ext import CallbackContext
from anekdot import get_anekdot
from harrypotterturbo import harrypotterturbo
from strelka_handler import STRELKA_REPLYS_LIST
from gpt_handler import get_gpt_response

SPECIAL_EVENTS_LIST = {
    "тупой бот": "тупой бот мамку твою ебет",
    "300": "отсоси у тракториста",
    "триста": "отсоси у тракториста",
    "бот пидор": "пидор у тебя в штанах",
    "вульва": "лол вульва",
    "вагина": "лол вагина она же почти вульва",
    "пизда": "да",
    "ПИДОР": "100% НАТУРАЛЬНАЯ ПИДРИЛА",
    "админ": "админ питух",
    "чо как": ["запор газы геморрой в жопе размером с грецкий орех а так норм", "пиздык хуяк", "напиши залупа"],    
    "ГА": ["в жопе панина нога", "буа га ГА", "крокодил залупа сыр"],
    "гараж": ["бля ща бы в гараж", "обожаю гараж и спидгараж", "как же хочется в гараж"],
    "Химмаш": ["химмаш это вам не уралмаш", "химаш не купиш не продаш", "химмаш ванлав"],
    "егор просвирнин": "1844!",
    "гарри поттер и": "harrypotterturbo",
    " я бы ": "handle_ya_by",
    "анек": "get_anekdot",
    "залупа": "get_anekdot",
    "саня": "handle_sanya",
    "сань": "handle_sanya",
    "александр": "handle_sanya",
    "шура": "handle_sanya",
    "шурик": "handle_sanya",
    "шуриг": "handle_sanya",
    "шурег": "handle_sanya",
    "шурек": "handle_sanya",
    "шурген": "handle_sanya",
    "санек": "handle_sanya",
    "санечка": "handle_sanya",
    "сася": "handle_sanya",
    "санчик": "handle_sanya",
    "санюшка": "handle_sanya",
    "саш": "handle_sanya",
    "саша": "handle_sanya",
    "сашка": "handle_sanya",
    "санчо": "handle_sanya",
    "санчес": "handle_sanya",
    "олександер": "handle_sanya",
    "олександро": "handle_sanya",
    "олександер": "handle_sanya",
    "алехандро": "handle_sanya",
}

STRELKA_TRIGGERS_LIST = ["завали", "заткнись", "задорнов", "гей", "геи"]

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
