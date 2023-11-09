import datetime
import aiogram
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import dp, bot
from data_base import sqlite_db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers import oplata
from keyboards.client_kb import kb_client_month, kb_client_month2, kb_client_month1, kb_client_day, kb_client_year
from keyboards.client_lk_kb import kb_client_lk

successful_payment_data = {}


class FSMAgain(StatesGroup):
    id_a = State()
    chanall_a = State()
    tariff_a = State()
    day_a = State()
    month_a = State()
    year_a = State()
    date_a = State()
    text_a = State()
    photo_a = State()


async def lk_register(message: types.Message):
    user_id = message.from_user.id
    count = sqlite_db.count_user_post(user_id)
    countotpr = sqlite_db.countotpr_user_post(user_id)
    await bot.send_message(message.from_user.id, f"Ваш id = {user_id}\nКол-во вышедших постов: {count}\nКол-во отправленных постов: {countotpr}", reply_markup=kb_client_lk)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("my_post"))
async def post(callback_query: types.CallbackQuery, state: FSMContext):
    id_tg = callback_query.from_user.id
    posts = await sqlite_db.all_post(id_tg)
    for elem_post in posts:
        global text_again
        text_again = elem_post[2]
        inline_keyboard = InlineKeyboardMarkup()
        sendpost = f'{elem_post[0]}_{elem_post[1]}'
        send_again_button = InlineKeyboardButton("Отправить еще раз !", callback_data=f"sendpost_{sendpost}")
        inline_keyboard.add(send_again_button)
        async with state.proxy() as data:
            data['photo_a'] = elem_post[4]
        formatted_text = elem_post[2]
        photo_file_id = elem_post[4]
        if photo_file_id:
            await bot.send_photo(819074198, photo=photo_file_id, caption=formatted_text,
                                 parse_mode=aiogram.types.ParseMode.HTML,
                                 reply_markup=inline_keyboard)
        else:
            await bot.send_message(819074198, formatted_text, parse_mode=aiogram.types.ParseMode.HTML,
                                   reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("sendpost_"))
async def send_post_again(callback_query: types.CallbackQuery, state: FSMContext):
    post_info = callback_query.data.split("_")[1:]
    print(post_info)
    async with state.proxy() as data:
        data['id_a'] = callback_query.message.chat.id
        data['chanall_a'] = post_info[0]
        data['tariff_a'] = post_info[1]
        data['text_a'] = text_again
    await FSMAgain.day_a.set()
    await bot.send_message(callback_query.from_user.id, "Введите дату в которую выйдет пост", reply_markup=kb_client_day)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("day_"), state=FSMAgain.day_a)
async def day_a(callback_query: types.CallbackQuery, state: FSMContext):
    day = callback_query.data.split("_")[1]
    print(day)
    async with state.proxy() as data:
        data['day_a'] = day
    await FSMAgain.month_a.set()
    if int(day) <= 28:
        await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите месяц',
                               reply_markup=kb_client_month)
    if 28 < int(day) < 31:
        await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите месяц',
                               reply_markup=kb_client_month2)
    if int(day) == 31:
        await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите месяц',
                               reply_markup=kb_client_month1)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("month_"), state=FSMAgain.month_a)
async def month_a(callback_query: types.CallbackQuery, state: FSMContext):
    month = callback_query.data.split("_")[1]
    print(month)
    async with state.proxy() as data:
        data['month_a'] = month
    await FSMAgain.year_a.set()
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите год', reply_markup=kb_client_year)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("year_"), state=FSMAgain.year_a)
async def year_a(callback_query: types.CallbackQuery, state: FSMContext):
    year = callback_query.data.split("_")[1]
    print(year)
    async with state.proxy() as data:
        data['year_a'] = year
    await load_date1(callback_query.message, state)


async def load_date1(message: types.Message, state: FSMContext):
    print('load_date')
    async with state.proxy() as data:
        day = data['day_a']
        month = data['month_a']
        year = data['year_a']
        data['date_a'] = f'{day}:{month}:{year}'
    current_datetime = datetime.datetime.now()
    async with state.proxy() as data:
        print(data['date_a'])
    try:
        print('прекол1')
        user_datetime = datetime.datetime.strptime(data['date_a'], '%d:%m:%Y')
        if user_datetime < current_datetime:
            await message.answer('Вы ввели дату в прошлом времени. Пожалуйста, введите текущую или будущую дату.', reply_markup=kb_client_day)
            await FSMAgain.day_a.set()
            return
        elif await sqlite_db.sql_date(data['chanall_a'], data['date_a']) == 0:
            await message.answer('Эта дата уже введена, попробуйте другую', reply_markup=kb_client_day)
            await FSMAgain.day_a.set()
            return
        else:
            print('прекол2')
            successful_payment_data[message.chat.id] = data
            await message.reply('Отлично, оплатите ваш пост')
            print(data['id_a'], data['chanall_a'], data['tariff_a'], data['date_a'], data['text_a'], data['photo_a'])
            await oplata.send_invoice(data['id_a'], data['chanall_a'], data['tariff_a'], data['date_a'], data['text_a'], data['photo_a'], 1)
            await state.finish()
    except ValueError:
        await message.answer('Неправильный формат даты. Введите дату в формате dd:mm:yyyy', reply_markup=kb_client_day)
        await FSMAgain.day_a.set()
        return

