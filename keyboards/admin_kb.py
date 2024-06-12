from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('отмена')

kb_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_admin.add(b1)
