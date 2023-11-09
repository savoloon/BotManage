from aiogram import types
from create_bot import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.client_kb import kb_client
from data_base import tech_db
import datetime


class FSMTech(StatesGroup):
    id_tech = State()
    text_tech = State()
    date_tech = State()


async def nach_tch(message: types.Message):
    await FSMTech.id_tech.set()
    await message.reply('Введите ваш вопрос или жалобу!')


@dp.message_handler(state=FSMTech.id_tech)
async def text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id_tech'] = message.from_user.id
        data['text_tech'] = message.text
        data['date_tech'] = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")
    await message.answer('Мы записали ваш вопрос или жалобу!', reply_markup=kb_client)
    async with state.proxy() as data:
        await tech_db.sql_add_tech(data['id_tech'], data['text_tech'], data['date_tech'])
    await state.finish()

