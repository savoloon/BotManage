import asyncio
from aiogram.utils import executor
from create_bot import dp
from handlers import client, other, post
from data_base import sqlite_db, sqlite_db_chanall, tech_db, post_opl, date_opl
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime


async def on_sturtup(_):
    print('Bot online')
    sqlite_db.sql_start()
    sqlite_db_chanall.sql_start()
    tech_db.sql_start()
    post_opl.sql_start()
    date_opl.sql_start()

client.register_handlers_client(dp)
other.register_handlers_other(dp)

scheduler = AsyncIOScheduler(time_zone='Europe/Moscow')
print('Hello')
print(datetime.now().hour, datetime.now().minute+1)
scheduler.add_job(post.scheduled_posts, trigger='cron', hour=11, minute=59)
scheduler.start()
loop = asyncio.get_event_loop()
loop.run_until_complete(executor.start_polling(dp, skip_updates=True, on_startup=on_sturtup))


