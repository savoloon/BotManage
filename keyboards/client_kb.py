from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


b1 = KeyboardButton('Разместить рекламу')
b51 = KeyboardButton('Личный кабинет')
b53 = KeyboardButton('Техподдержка')
b56 = KeyboardButton('Администратор')

b2 = InlineKeyboardButton(text='1', callback_data='day_1')
b3 = InlineKeyboardButton(text='2', callback_data='day_2')
b4 = InlineKeyboardButton(text='3', callback_data='day_3')
b5 = InlineKeyboardButton(text='4', callback_data='day_4')
b6 = InlineKeyboardButton(text='5', callback_data='day_5')
b7 = InlineKeyboardButton(text='6', callback_data='day_6')
b8 = InlineKeyboardButton(text='7', callback_data='day_7')
b9 = InlineKeyboardButton(text='8', callback_data='day_8')
b10 = InlineKeyboardButton(text='9', callback_data='day_9')
b11 = InlineKeyboardButton(text='10', callback_data='day_10')
b12 = InlineKeyboardButton(text='11', callback_data='day_11')
b13 = InlineKeyboardButton(text='12', callback_data='day_12')
b14 = InlineKeyboardButton(text='13', callback_data='day_13')
b15 = InlineKeyboardButton(text='14', callback_data='day_14')
b16 = InlineKeyboardButton(text='15', callback_data='day_15')
b17 = InlineKeyboardButton(text='16', callback_data='day_16')
b18 = InlineKeyboardButton(text='17', callback_data='day_17')
b19 = InlineKeyboardButton(text='18', callback_data='day_18')
b20 = InlineKeyboardButton(text='19', callback_data='day_19')
b21 = InlineKeyboardButton(text='20', callback_data='day_20')
b22 = InlineKeyboardButton(text='21', callback_data='day_21')
b23 = InlineKeyboardButton(text='22', callback_data='day_22')
b24 = InlineKeyboardButton(text='23', callback_data='day_23')
b25 = InlineKeyboardButton(text='24', callback_data='day_24')
b26 = InlineKeyboardButton(text='25', callback_data='day_25')
b27 = InlineKeyboardButton(text='26', callback_data='day_26')
b28 = InlineKeyboardButton(text='27', callback_data='day_27')
b29 = InlineKeyboardButton(text='28', callback_data='day_28')
b30 = InlineKeyboardButton(text='29', callback_data='day_29')
b31 = InlineKeyboardButton(text='30', callback_data='day_30')
b32 = InlineKeyboardButton(text='31', callback_data='day_31')


b35 = InlineKeyboardButton('Январь', callback_data='month_01')
b36 = InlineKeyboardButton('Февраль', callback_data='month_02')
b37 = InlineKeyboardButton('Март', callback_data='month_03')
b38 = InlineKeyboardButton('Апрель', callback_data='month_04')
b39 = InlineKeyboardButton('Май', callback_data='month_05')
b40 = InlineKeyboardButton('Июнь', callback_data='month_06')
b41 = InlineKeyboardButton('Июль', callback_data='month_07')
b42 = InlineKeyboardButton('Август', callback_data='month_08')
b43 = InlineKeyboardButton('Сентябрь', callback_data='month_09')
b44 = InlineKeyboardButton('Октябрь', callback_data='month_10')
b45 = InlineKeyboardButton('Ноябрь', callback_data='month_11')
b46 = InlineKeyboardButton('Декабрь', callback_data='month_12')


b47 = InlineKeyboardButton('2023', callback_data='year_2023')
b48 = InlineKeyboardButton('2024', callback_data='year_2024')
b49 = InlineKeyboardButton('2025', callback_data='year_2025')
b50 = InlineKeyboardButton('2026', callback_data='year_2026')

b54 = InlineKeyboardButton('Да', callback_data='photo_1')
b55 = InlineKeyboardButton('Нет', callback_data='photo_2')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(b1).row(b51, b53)
kb_client_admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b1, b56).row(b51, b53)
kb_client_day = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b2, b3, b4, b5, b6, b7, b8).row(b9, b10,b11,b12,b13,b14,b15).row(b16,b17,b18,b19,b20,b21,b22).row(b23,b24,b25,b26,b27,b28).row(b29,b30,b31,b32)
kb_client_month = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b35, b36, b37, b38).row(b39, b40, b41, b42).add(b43, b44, b45, b46)
kb_client_month1 = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b35, b37, b39, b41).row(b42, b44, b46)
kb_client_month2 = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b35,b37,b38).row(b39,b40,b41,b42).add(b43,b44,b45,b46)
kb_client_year = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b47, b48).row(b49,b50)
kb_client_photo = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(b54, b55)



