import datetime
from pyrogram import Client
from pyrogram.enums import ChatType
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from create_bot import dp, bot
from keyboards.client_kb import kb_client, kb_client_day, kb_client_month, kb_client_year, \
    kb_client_month2, kb_client_month1, kb_client_admin
from data_base import sqlite_db, sqlite_db_chanall
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.lk_clientpost import lk_register
from handlers.tech import nach_tch
from data_base import date_opl
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

TARGET_USER_ID = int(os.getenv("VLAD"))

api_id = '24401161'
api_hash = 'da5e0c071a34838534f6a58da3934af8'
phone = '+79378427880'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, phone_number=phone)


class FSMClient(StatesGroup):
    id = State()
    chanall = State()
    tariff = State()
    day = State()
    month = State()
    year = State()
    date = State()
    photo = State()
    formatted_text = State()
    text = State()


async def make_changes_command(message: types.Message):
    if message.from_user.id == TARGET_USER_ID:
        await bot.send_message(message.from_user.id, "Здравствуйте!\nНапишите слово 'отмена', если хотите выйти в главное меню отменив результат.", reply_markup=kb_client_admin)
    else:
        await bot.send_message(message.from_user.id, "Здравствуйте!", reply_markup=kb_client)



async def lk_client(message: types.Message):
    await lk_register(message)


async def tech(message: types.Message):
    await nach_tch(message)


async def cm_start(message: types.Message):
    kb_client_chanall = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    channel_list = sqlite_db_chanall.chanall_slc()
    print(channel_list)
    for channel_name in channel_list:
        kb_client_chanall.add(InlineKeyboardButton(channel_name[0], callback_data=f"channel_{channel_name[0]}"))
    await FSMClient.chanall.set()
    await message.reply('Выберите канал', reply_markup=kb_client_chanall)


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("channel_"), state="*")
async def load_chanall(callback_query: types.CallbackQuery, state: FSMContext):
    channel = callback_query.data.split("_")[1]
    async with state.proxy() as data:
        data['id'] = callback_query.message.chat.id
        data['chanall'] = channel
        try:
            id_chan = sqlite_db_chanall.id_ch(data['chanall'])
        except Exception as e:
            id_chan = 0
    if id_chan:
        members_count = await bot.get_chat_members_count(chat_id=int(id_chan[0]))
        async with app:
            message_week = 0
            chat = await app.get_chat(int(id_chan[0]))
            time = datetime.now()
            messages = app.get_chat_history(int(id_chan[0]))
            a = []
            b = 0
            print(chat.type)
            if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
                print('ГРУППА')
                async for message in messages:
                    if message.date >= time - timedelta(weeks=1):
                        message_week += 1
                        if message.from_user:
                            a.append(message.from_user.id)
                            print(a)
            if chat.type == ChatType.CHANNEL:
                print('КАНААААЛ')
                async for message in messages:
                    if message.date >= time - timedelta(weeks=1):
                        message_week += 1
                        print(message.views)
                        if message.views:
                            b += int(message.views)
            unique_set = set(a)
            unique_list = list(unique_set)
    kb_client_tarif = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    async with state.proxy() as data:
        tarif_list = sqlite_db_chanall.tarif_slc(data['chanall'])
    print(tarif_list)
    for tarif_name in tarif_list:
        print(tarif_name[0])
        tarif_name = tarif_name[0].split(', ')
        print(tarif_name)
        for elem in tarif_name:
            kb_client_tarif.add(InlineKeyboardButton(elem, callback_data=f"tarif_{elem}"))
    await FSMClient.next()
    if id_chan:
        start_date = time - timedelta(weeks=1)
        end_date = time
        date_range = f"{start_date.strftime('%d:%m:%Y')} - {end_date.strftime('%d:%m:%Y')}"
        if chat.type == ChatType.GROUP or chat.type == ChatType.SUPERGROUP:
            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text=f'\n{date_range}\nКоличество подписчиков в этом канале: {members_count}\nКол-во сообщений за неделю: {message_week}\nКол-во пользователей, которые отправляли сообщение: {len(unique_list)}')
        elif chat.type == ChatType.CHANNEL:
            await bot.send_message(chat_id=callback_query.message.chat.id,
                                   text=f'\n{date_range}\nКоличество подписчиков в этом канале: {members_count}\nКол-во сообщений за неделю: {message_week}\nКол-во просмотров за неделю: {b}')
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Теперь введи тариф', reply_markup=kb_client_tarif)



@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("tarif_"), state="*")
async def load_tariff(callback_query: types.CallbackQuery, state: FSMContext):
    tarif = callback_query.data.split("_")[1]
    async with state.proxy() as data:
        data['tariff'] = tarif
    await FSMClient.day.set()
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Теперь выберите день в который вы хотите,чтобы ваш пост вышел', reply_markup=kb_client_day)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("day_"), state="*")
async def day(callback_query: types.CallbackQuery, state: FSMContext):
    day = callback_query.data.split("_")[1]
    print(day)
    async with state.proxy() as data:
        data['day'] = day
    await FSMClient.month.set()
    if int(day) <= 28:
        await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите месяц',
                               reply_markup=kb_client_month)
    if 28 < int(day) < 31:
        await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите месяц',
                               reply_markup=kb_client_month2)
    if int(day) == 31:
        await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите месяц',
                               reply_markup=kb_client_month1)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("month_"), state="*")
async def month(callback_query: types.CallbackQuery, state: FSMContext):
    month = callback_query.data.split("_")[1]
    print(month)
    async with state.proxy() as data:
        data['month'] = month
    await FSMClient.year.set()
    await bot.send_message(chat_id=callback_query.message.chat.id, text='Выберите год', reply_markup=kb_client_year)


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith("year_"), state="*")
async def year(callback_query: types.CallbackQuery, state: FSMContext):
    year = callback_query.data.split("_")[1]
    print(year)
    async with state.proxy() as data:
        data['year'] = year
    await load_date(callback_query.message, state)


async def load_date(message: types.Message, state: FSMContext):
    print('load_date')
    async with state.proxy() as data:
        day = data['day']
        month = data['month']
        year = data['year']
        data['date'] = f'{day}:{month}:{year}'
    current_datetime = datetime.datetime.now()
    async with state.proxy() as data:
        print(data['date'])
    try:
        print('прекол1')
        user_datetime = datetime.datetime.strptime(data['date'], '%d:%m:%Y')
        if user_datetime <= current_datetime:
            await message.answer('Вы ввели дату в прошлом времени. Пожалуйста, введите текущую или будущую дату.', reply_markup=kb_client_day)
            await FSMClient.day.set()
            return
        elif await date_opl.sql_date(data['chanall'], data['date']) == 0:
            await message.answer('Эта дата уже введена, попробуйте другую', reply_markup=kb_client_day)
            await FSMClient.day.set()
            return
        else:
            print('прекол2')
            await message.reply('Отправьте пост')
            await FSMClient.text.set()
    except ValueError:
        await message.answer('Неправильный формат даты. Введите дату в формате dd:mm:yyyy', reply_markup=kb_client_day)
        await FSMClient.day.set()
        return


@dp.message_handler(content_types=[types.ContentType.PHOTO], state=FSMClient.text)
async def load_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_id'] = message.message_id
        if message.photo:
            data['photo'] = message.photo[-1].file_id
        else:
            data['photo'] = None
        formatted_text = message.html_text
        data['formatted_text'] = formatted_text
        await message.answer('Мы отправили ваше предложение администратору!', reply_markup=kb_client)
    async with state.proxy() as data:
        await sqlite_db.sql_add_command(data['id'], data['chanall'], data['tariff'], data['date'], data['formatted_text'], data['photo'])
    await state.finish()


@dp.message_handler(content_types=[types.ContentType.TEXT], state=FSMClient.text)
async def load_text_without_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message_id'] = message.message_id
        data['photo'] = None
        formatted_text = message.html_text
        data['formatted_text'] = formatted_text
        await message.answer('Мы отправили ваше предложение администратору!', reply_markup=kb_client)
    async with state.proxy() as data:
        await sqlite_db.sql_add_command(data['id'], data['chanall'], data['tariff'], data['date'], data['formatted_text'], None)
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cm_start, text=['Разместить рекламу'], state=None)
    dp.register_message_handler(lk_client, text=['Личный кабинет'], state=None)
    dp.register_message_handler(tech, text=['Техподдержка'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_chanall, state=FSMClient.chanall)
    dp.register_message_handler(load_tariff, state=FSMClient.tariff)
    dp.register_message_handler(load_date, state=FSMClient.date)
    dp.register_message_handler(make_changes_command, commands=['start'])
