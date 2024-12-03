from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def request_movie() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text='Найти')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(button_1)

    return keyboard