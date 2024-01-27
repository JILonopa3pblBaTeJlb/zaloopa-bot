import random
import re

def handle_debil_mode(text, context):
    if context.bot_data.get('debil_mode'):
        text = re.sub(r'[^\w\s]', '', text).lower()
        text = text.replace('\n', ' ').replace('\r', '')

        # Удаление каждого 10-го знака с вероятностью 0.1 для каждого символа
        text = ''.join(char for i, char in enumerate(text) if (i + 1) % 10 != 0 or random.random() > 0.1)
        
        # Замена символов а=о, о=а, и=е, е=и с вероятностью 0.01 для каждого символа
        char_map = {'а': 'о', 'о': 'а', 'и': 'е', 'е': 'и'}
        num_replacements = int(len(text) * 0.1)
        replace_indices = random.sample(range(len(text)), num_replacements)
        text = ''.join(char_map[char] if i in replace_indices and char in char_map else char for i, char in enumerate(text))
        
        # Безусловная замена "ться" на "ца" и "тся" на "ццо"
        text = text.replace('ться', 'ца').replace('тся', 'ццо')
        
        # Удаление пробелов с вероятностью 0.1
        text = ''.join(char if char != ' ' or random.random() > 0.05 else '' for char in text)
        
        additional_words = ["нахуй", "сукбля", "сцук", "бля", "бля нахуй ебать", "епта", "епты", "епт"]
        words = text.split()
        for i in range(4, len(words), 6):
            insert_word = random.choice(additional_words)
            words.insert(i, insert_word)
        text = ' '.join(words)

    return text
