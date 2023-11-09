import asyncio
import aiogram
from create_bot import bot
from datetime import datetime, timedelta
from data_base import post_opl
from data_base import sqlite_db_chanall


async def send_scheduled_post(channel_id, message_tarif,message_text, message_photo):
    if message_photo:
        message = await bot.send_photo(int(channel_id[0]), photo=message_photo, caption=message_text,
                             parse_mode=aiogram.types.ParseMode.HTML)
    else:
        message = await bot.send_message(int(channel_id[0]), message_text, parse_mode=aiogram.types.ParseMode.HTML)
    try:
        print(channel_id)
        await bot.pin_chat_message(chat_id=int(channel_id[0]), message_id=message.message_id)
        await asyncio.sleep(24*60*60)
        await bot.unpin_chat_message(chat_id=int(channel_id[0]), message_id=message.message_id)
    except Exception as e:
        print(e.args)
    try:
        if message_tarif[0] == 'На день':
            await asyncio.sleep(24*60*60)
            bot.delete_message(chat_id=int(channel_id[0]), message_id=message.message_id)
        elif message_tarif[0] == 'На 2 дня':
            await asyncio.sleep(24 * 60 * 60 * 2)
            bot.delete_message(chat_id=int(channel_id[0]), message_id=message.message_id)
        elif message_tarif[0] == 'На неделю' or message_tarif == 'На месяц':
            await asyncio.sleep(24 * 60 * 60 * 7)
            bot.delete_message(chat_id=int(channel_id[0]), message_id=message.message_id)
    except Exception as e:
        print(e.args)


async def send_scheduled_post1(channel_id, message_tarif,message_text, message_photo):
    if message_photo:
        message = await bot.send_photo(int(channel_id[0]), photo=message_photo, caption=message_text,
                             parse_mode=aiogram.types.ParseMode.HTML)
    else:
        message = await bot.send_message(int(channel_id[0]), message_text, parse_mode=aiogram.types.ParseMode.HTML)
    try:
        print(channel_id)
        await bot.pin_chat_message(chat_id=int(channel_id[0]), message_id=message.message_id)
        await asyncio.sleep(24*60*60)
        await bot.unpin_chat_message(chat_id=int(channel_id[0]), message_id=message.message_id)
    except Exception as e:
        print(e.args)
    try:
        if message_tarif[0] == 'На месяц':
            await asyncio.sleep(24*60*60*2)
            bot.delete_message(chat_id=int(channel_id[0]), message_id=message.message_id)
    except Exception as e:
        print(e.args)


async def scheduled_posts():
    print('Ничего не понятно')
    records = post_opl.all_opl()
    print(records)
    today = datetime.now().date()
    print(today)
    tasks = []
    for record in records:
        channel_id = sqlite_db_chanall.id_ch(record[1])
        print(record)
        print(channel_id)
        date_str = record[2]
        message_text = record[3]
        message_photo = record[4]
        message_tarif = record[5]
        date_obj = datetime.strptime(date_str, "%d:%m:%Y").date()
        print(date_obj)
        if message_tarif != 'На месяц':
            if date_obj == today:
                asyncio.create_task(send_scheduled_post(channel_id, message_tarif, message_text, message_photo))
        else:
            date_list = [date_obj + timedelta(days=7 * i) for i in range(5)]
            for i, date in enumerate(date_list):
                if today == date:
                    if i != 4:
                        asyncio.create_task(send_scheduled_post(channel_id, message_tarif, message_text, message_photo))
                    else:
                        asyncio.create_task(send_scheduled_post1(channel_id, message_tarif, message_text, message_photo))
    await asyncio.gather(*tasks)

