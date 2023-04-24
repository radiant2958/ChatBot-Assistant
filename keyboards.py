from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Создаем основную клавиатуру с кнопками для главного меню
keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)


# Создаем кнопки для основной клавиатуры
btn_weather = KeyboardButton('/weather')
btn_currency = KeyboardButton('/exchange')
btn_animals = KeyboardButton('/image_animal')
btn_poll = KeyboardButton('/create_poll')

# Добавляем созданные кнопки на основную клавиатуру
keyboard.add(btn_weather, btn_currency, btn_animals, btn_poll)

# Создаем клавиатуру для выбора валюты
keyboard_currency = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

# Создаем кнопки для клавиатуры выбора валюты
btn_usd = KeyboardButton('USD')  # Доллар США
btn_eur = KeyboardButton('EUR')  # Евро
btn_rub = KeyboardButton('RUB')  # Российский рубль
btn_cny = KeyboardButton('CNY')  # Китайский юань

# Добавляем созданные кнопки на клавиатуру выбора валюты
keyboard_currency.add(btn_usd, btn_eur, btn_rub, btn_cny)
