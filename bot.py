from aiogram import Bot, Dispatcher
from os import getenv
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = getenv('API_TOKEN')
API_KEY = getenv('API_KEY')

bot = Bot('API_TOKEN')
dp = Dispatcher(bot)
