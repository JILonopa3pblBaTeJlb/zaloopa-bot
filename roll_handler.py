import random
from telegram import Update
from telegram.ext import CallbackContext

gay_emojis = ['🧔‍♀️', '👰🏻‍♂️', '👯‍♂️', '👬', '👨‍❤️‍👨', '💑', '👨‍❤️‍💋‍👨', '🌈', '🤼‍♂️', '💝', '🏳️‍🌈', '🫂', '👥']
vegetable_emojis = ['🍆', '🌶', '🥒', '🥕', '🌽', '🥖', '🍌', '🍾']

def roll_emojis():
    selected_set = random.choices([gay_emojis, vegetable_emojis], weights=[15, 5])[0]
    roll_chance = random.random()
    if roll_chance <= 0.0001:
        return ['🌈'] * 3
    elif roll_chance <= 0.1:
        emoji = random.choice(selected_set)
        return [emoji, emoji, emoji]
    return random.sample(selected_set, 3)

def roll(update: Update, context: CallbackContext):
    emoji_list = roll_emojis()
    rolled_emojis = ''.join(emoji_list)
    message_id = update.message.message_id
    chat_id = update.message.chat_id

    context.bot.send_message(chat_id=chat_id, text=rolled_emojis, reply_to_message_id=message_id)

    user_first_name = update.message.from_user.first_name
    if rolled_emojis == '🌈🌈🌈':
        reply_text = f"🎉ПОЗДРОВЛЕНИЯ ОТ 1хбот!!! 🎉{user_first_name} ТЫ СУПИРПИДОР! 🎉"
        context.bot.send_message(chat_id=chat_id, text=reply_text, reply_to_message_id=message_id)
    elif len(set(emoji_list)) == 1:
        winning_message = f"ПОЗДРОВЛЕНИЕ ОТ 1хбот тебе {user_first_name}! ТЫ ПИДОР {rolled_emojis}"
        context.bot.send_message(chat_id=chat_id, text=winning_message, reply_to_message_id=message_id)
