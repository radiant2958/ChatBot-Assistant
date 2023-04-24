import asyncio
import os
import random
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove
from create import dp, API_KEY, bot
from aiogram import types
from keyboards import keyboard
from utils import get_weather, process_currency_conversion

#Обработчик команды '/start'
# Отправляет приветственное сообщение с клавиатурой, позволяющей выбрать, что именно пользователь хочет сделать.
@dp.message_handler(commands='start')
async def mes_start(message: types.Message):
    await message.answer(
        "Привет! Я помогу тебе в нескольких задачах. Выбери, что тебя интересует:",
        reply_markup=keyboard)

# Обработчик команды '/weather'
# Отправляет сообщение с запросом названия города, в ответ на которое вызывается
# функция get_city_weather, которая получает информацию о погоде из API openweathermap и возвращает ее в чат.
@dp.message_handler(commands=['weather'])
async def mes_weather(message: types.Message):
    await message.answer('Введите название города', reply_markup=ReplyKeyboardRemove())
    @dp.message_handler()
    async def get_city_weather(message: types.Message):
        try:
            city = message.text
            weather = await get_weather(city, API_KEY)
            await message.answer(weather)
            await message.answer('Чем я могу еще помочь:', reply_markup=keyboard)
        except Exception as e:
            await message.answer(f"Ошибка: {e}")


# Обработчик команды '/exchange'
# Создает задачу на выполнение функции process_currency_conversion, которая обрабатывает конвертацию валют.
@dp.message_handler(commands=['exchange'])
async def convert_currency_handler(message: types.Message):
    try:
        await process_currency_conversion(message)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


# Обработчик команды '/image_animal'
# Отправляет случайное изображение животного из локальной директории с изображениями.
@dp.message_handler(commands=['image_animal'])
async def send_random_animal_image(message: types.Message):
    try:
        image_directory = r'C:\Users\kandy\Desktop\pythonProject1\images'
        animal_images = os.listdir(image_directory)
        image_name = random.choice(animal_images)
        image_path = os.path.join(image_directory, image_name)
        chat_id = message.chat.id
        with open(image_path, 'rb') as photo:
            await bot.send_photo(chat_id=chat_id, photo=photo, reply_markup=types.ReplyKeyboardRemove())
            await message.answer('Чем я могу еще помочь:', reply_markup=keyboard)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


# Обработчик создания опроса
# Использует состояние PollState, которое представляет собой конечный автомат,
# чтобы пользователь мог последовательно вводить необходимые данные для создания опроса: id чата, вопрос и варианты ответов.
# После ввода всех необходимых данных бот отправляет опрос в указанный чат.


class PollState(StatesGroup):
    enter_chat_id = State()
    enter_poll_question = State()
    enter_poll_options = State()


@dp.message_handler(Command('create_poll'))
async def create_poll_handler(message: types.Message):
    try:
        await message.answer("Введите ID чата, в который вы хотите отправить опрос:",
                             reply_markup=ReplyKeyboardRemove())
        await PollState.enter_chat_id.set()
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@dp.message_handler(lambda message: message.text.isdigit(), state=PollState.enter_chat_id)
async def enter_chat_id(message: types.Message, state: FSMContext):
    try:
        chat_id = int(message.text)
        await state.update_data(chat_id=chat_id)

        await message.answer("Введите вопрос для опроса:")
        await PollState.enter_poll_question.set()
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@dp.message_handler(lambda message: not message.text.isdigit(), state=PollState.enter_poll_question)
async def enter_poll_question(message: types.Message, state: FSMContext):
    try:
        question = message.text
        await state.update_data(question=question)

        await message.answer("Введите варианты ответов через запятую:")
        await PollState.enter_poll_options.set()
    except Exception as e:
        await message.answer(f"Ошибка: {e}")


@dp.message_handler(lambda message: not message.text.isdigit(), state=PollState.enter_poll_options)
async def enter_poll_options(message: types.Message, state: FSMContext):
    try:
        options_text = message.text
        options = [option.strip() for option in options_text.split(',')]

        user_data = await state.get_data()
        chat_id = user_data['chat_id']
        question = user_data['question']

        # Создать опрос
        await bot.send_poll(chat_id=chat_id, question=question, options=options)

        # Завершить состояние и спросить пользователя, что еще он хочет сделать
        await message.answer("Опрос создан!")
        await message.answer('Чем я могу еще помочь:', reply_markup=keyboard)
        await state.finish()
    except Exception as e:
        await message.answer(f"Ошибка: {e}")
