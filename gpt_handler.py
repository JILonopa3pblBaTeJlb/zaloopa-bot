import random
import g4f
import re
from time import time
from dialogue_handler import DIALOGUE_LIST
from debil_mode import handle_debil_mode

PROVIDERS = ['Liaobots', 'GeekGpt']
last_gpt_response_time = 0

def get_gpt_response(prompt, update, context):
    global last_gpt_response_time
    current_time = time()
    chat_data = context.chat_data

    if current_time - last_gpt_response_time < 60:
        return random.choice(DIALOGUE_LIST)

    for _ in range(5):
        try:
            with open('prompt.txt', 'r') as f:
                preprompt = f.read()
            selected_provider = random.choice(PROVIDERS)
            model = getattr(g4f.models, "gpt_4")
            provider = getattr(g4f.Provider, selected_provider)
            start_time = time()
            response = g4f.ChatCompletion.create(
                model=model,
                provider=provider,
                messages=[{"role": "user", "content": preprompt + prompt}],
            )
            last_gpt_response_time = current_time
            context.bot_data['last_gpt_response_time'] = last_gpt_response_time
            return handle_debil_mode(response, context)
        except Exception:
            continue
    return random.choice(DIALOGUE_LIST)
