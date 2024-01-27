import requests
import re
import json
from debil_mode import handle_debil_mode  # Импортируйте handle_debil_mode

def get_anekdot():
    try:
        response = requests.get('https://www.anekdot.ru/rss/random.html')
        text = response.content.decode('windows-1251')
        json_string_match = re.search(r'JSON\.parse\(\'(.+?)\'\);', text, re.DOTALL)
        if json_string_match:
            json_string = json_string_match.group(1).replace("\\'", "'").replace('\\"', '"').replace('\\\\', '\\')
            anekdot_text = json.loads(json_string)[0].replace('<br>', '\n')

            # Создайте фиктивный контекст для использования с handle_debil_mode
            dummy_context = type('Dummy', (object,), {'bot_data': {'debil_mode': True}})()

            # Примените handle_debil_mode к тексту анекдота
            anekdot_text = handle_debil_mode(anekdot_text, dummy_context)

            return anekdot_text
        return "залупа не найдена"
    except Exception as e:
        return f"Ошибка при получении залупы: {e}"
