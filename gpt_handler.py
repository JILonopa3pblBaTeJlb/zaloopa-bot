import random
import g4f
import logging
import time
from dialogue_handler import DIALOGUE_LIST
from debil_mode import handle_debil_mode
from config import LOG_MODE, TEST_MODEG4F
#import ssl
#ssl._create_default_https_context = ssl._create_unverified_context


logging.basicConfig(level=logging.INFO)


last_gpt_response_time = 0

def mark_provider_as_failed(failed_provider):
    if TEST_MODEG4F == 0:  # Если TEST_MODEG4F не активирован, отмечаем провайдера как неработающий
        with open('providers_list.txt', 'r') as file:
            providers = file.readlines()
        providers = ['#' + p if p.strip() == failed_provider and not p.startswith('#') else p for p in providers]
        with open('providers_list.txt', 'w') as file:
            file.writelines(providers)
        if LOG_MODE:
            logging.info(f"Провайдер {failed_provider} отмечен как неработающий")
    else:
        if LOG_MODE:
            logging.info(f"TEST_MODEG4F активирован: Пропускаем отметку провайдера {failed_provider} как неработающий")

import time

def get_gpt_response(prompt, update, context):
    global last_gpt_response_time
    current_time = time.time()
    chat_data = context.chat_data

    if LOG_MODE:
        logging.info("Получение ответа GPT начато")

    if current_time - last_gpt_response_time < 60:
        if LOG_MODE:
            logging.info("Возвращаем сообщение из DIALOGUE_LIST так как последний ответ был менее 60 секунд назад")
        return handle_debil_mode(random.choice(DIALOGUE_LIST), context)

    with open('providers_list.txt', 'r') as file:
        providers = [line.strip() for line in file]

    selected_provider = None
    provider_response_time = None

    for _ in range(5):
        try:
            with open('prompt.txt', 'r') as f:
                preprompt = f.read()

            active_providers = [p for p in providers if not p.startswith('#')]
            if not active_providers:
                raise Exception("Все провайдеры были отмечены как неработающие.")

            selected_provider = random.choice(active_providers)
            if LOG_MODE:
                logging.info(f"Выбран провайдер: {selected_provider}")
            model = getattr(g4f.models, "gpt_4")
            provider = getattr(g4f.Provider, selected_provider)
            start_time = time.time()
            response = g4f.ChatCompletion.create(
                model=model,
                provider=provider,
                messages=[{"role": "user", "content": preprompt + prompt}],
            )
            provider_response_time = time.time() - start_time
            if provider_response_time > 55:
                if LOG_MODE:
                    logging.info(f"Время ответа провайдера {selected_provider} превысило 55 секунд.")
                continue
            last_gpt_response_time = current_time
            context.bot_data['last_gpt_response_time'] = last_gpt_response_time
            return handle_debil_mode(response, context)
        except Exception as e:
            if LOG_MODE:
                logging.error(f"Ошибка при работе с провайдером {selected_provider}: {e}")
            if selected_provider:
                mark_provider_as_failed(selected_provider)
            continue

    if LOG_MODE:
        logging.info("Все попытки неудачны, возвращаем случайное сообщение из DIALOGUE_LIST")
    return handle_debil_mode(random.choice(DIALOGUE_LIST), context)
