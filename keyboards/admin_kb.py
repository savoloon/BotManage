from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


b3 = KeyboardButton('/Принять')
b4 = KeyboardButton('/Отказать')

b5 = InlineKeyboardButton(text='ЮКасса', callback_data='money_1')
b6 = InlineKeyboardButton(text='Криптовалюта', callback_data='money_2')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True).add(b3).add(b4)
check_opl = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(b5, b6)
