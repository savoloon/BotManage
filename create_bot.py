from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
from dotenv import load_dotenv

storage = MemoryStorage()
load_dotenv()

bot = Bot(os.getenv("BOT"))
dp = Dispatcher(bot, storage=storage)

