import random
import re

def handle_debil_mode(text, context):
    if context.bot_data.get('debil_mode'):
        text = re.sub(r'[^\w\s]', '', text).lower().replace('\n', ' ').replace('\r', ' ')
        
        char_map = {'а': 'о', 'о': 'а', 'и': 'е', 'е': 'и'}
        words = text.split()
        text = ' '.join(''.join(char_map[char] if char in char_map and random.random() < 0.05 else char for char in word) if len(word) > 4 else word for word in words)

        words = text.split()
        text = ' '.join(''.join(char for i, char in enumerate(word) if (i + 1) % 5 != 0 or random.random() > 0.02) if len(word) > 3 else word for word in words)
        
        text = text.replace('ться', 'ца').replace('тся', 'ццо')
        text = ''.join(char if char != ' ' or random.random() > 0.02 else '' for char in text)
        
        char_replacement_map = {'а': 'ва', 'ы': 'ыф', 'ч': 'чс', 'р': 'пр', 'д': 'дж', 'т': 'ть'}
        text = ''.join(char_replacement_map[char] if char in char_replacement_map and random.random() < 0.01 else char for char in text)
        
        words = text.split()
        new_words = []
        for i, word in enumerate(words):
            new_words.append(word)
            if (i + 1) % 3 == 0 and len(word) > 3:
                new_words.append(random.choice(["нахуй", "сукбля", "сцук", "бля", "бля нахуй ебать", "епта", "епты", "епт"]))
        
        text = ' '.join(new_words) + ' ' + ' '.join(random.sample(["ебать", "сук", "бля", "нахуй", "псдц"], k=3))

    return text
