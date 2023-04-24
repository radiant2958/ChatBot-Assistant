from aiogram import types
import aiohttp
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardRemove

from create import dp, bot
from keyboards import keyboard_currency, keyboard

# Функция для асинхронного запроса JSON данных
async def fetch_json(session, url):
    async with session.get(url) as response:
        if response.status != 200:
            raise ValueError(f"Ошибка при получении данных. Код ответа: {response.status}")
        return await response.json()


# Функция для получения погоды из API
async def get_weather(city_name, api_key) -> str:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric&lang=ru"
            data = await fetch_json(session, url)

            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            temp_min = data['main']['temp_min']
            temp_max = data['main']['temp_max']
            main = data['weather'][0]['main']
            description = data['weather'][0]['description']

            return f"Сейчас температура равна: {temp} градусов Цельсия\n" \
                   f"ощущается как {feels_like} градусов Цельсия\n" \
                   f"минимальная температура сегодня равна: {temp_min} градусов Цельсия\n" \
                   f"максимальная температура сегодня равна: {temp_max} градусов Цельсия\n" \
                   f"на небе {description}"

# Функция для обработки конвертации валюты
async def process_currency_conversion(message: types.Message):
    await message.answer('Выбери валюту для конвертации:', reply_markup=keyboard_currency)
    from_currency = ''
    to_currency = ''
    amount = 0

    # Функция для выбора валюты для конвертации
    async def choose_currency(message: types.Message):
        nonlocal from_currency, to_currency
        if not from_currency:
            from_currency = message.text
            await message.answer('Выбери валюту в которую конвертировать:', reply_markup=keyboard_currency)
        else:
            to_currency = message.text
            await message.answer('Введи сумму для конвертации', reply_markup=ReplyKeyboardRemove())

    # Функция для конвертации валюты с использованием API
    async def convert_currency(from_currency, to_currency, amount):
        async with aiohttp.ClientSession() as session:
            url = f'https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}'
            data = await fetch_json(session, url)
            result = data['result']
            return result

    # Функция для ввода суммы и вывода результата конвертации
    async def enter_amount(message: types.Message):
        nonlocal amount
        amount = float(message.text)
        result = await convert_currency(from_currency,to_currency,amount)
        await message.answer(f"{from_currency} {to_currency} = {result} {amount}")
        await message.answer('Чем я могу еще помочь:', reply_markup=keyboard)

    # Регистрация обработчиков сообщений для выбора валюты и ввода суммы
    dp.register_message_handler(choose_currency, Text(equals=["USD", "EUR", "RUB", "CNY"]))
    dp.register_message_handler(enter_amount, lambda message: message.text.isdigit())

