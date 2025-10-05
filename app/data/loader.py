from aiogram import Bot, Dispatcher, F
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os


load_dotenv()


bot = Bot(token=os.getenv('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

