import re
from telegram import Update
from telegram.ext import CallbackContext

def contains_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def lexical_reduplication(word):
    if len(word) > 20 or not contains_cyrillic(word):
        return None

    vowels = "аеёиоуыэюя"
    vowel_mapping = {v: v for v in vowels}
    vowel_mapping.update({"о": "ё", "у": "ю", "э": "е"})

    first_vowel_index = next((i for i, char in enumerate(word) if char.lower() in vowels), None)

    if first_vowel_index is None:
        return word

    first_vowel = word[first_vowel_index].lower()
    mapped_vowel = vowel_mapping.get(first_vowel, first_vowel)

    new_word = "ху" + ("" if first_vowel_index == 1 else "й") + mapped_vowel + word[first_vowel_index:]

    new_word = "".join(new_word[i] for i in range(len(new_word)) if i == 0 or new_word[i] != new_word[i - 1])
    new_word = new_word.replace("ёо", "ё").replace("йю", "ю").replace("яа", "я").replace("юу", "ю").replace("йе", "е")

    return new_word.capitalize() if word[0].isupper() else new_word

def reduplicate(update: Update, context: CallbackContext):
    last_word = re.findall(r'\b\w+\b', update.message.text)[-1]
    reduplicated_word = lexical_reduplication(last_word)
    if reduplicated_word:
        update.message.reply_text(reduplicated_word)
