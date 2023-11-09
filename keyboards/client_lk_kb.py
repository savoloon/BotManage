from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup

c2 = InlineKeyboardButton(text='Мои посты', callback_data='my_post')

kb_client_lk = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(c2)
