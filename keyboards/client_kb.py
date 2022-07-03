from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from data_base import db

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Внести данные'),
            KeyboardButton(text='Просмотр данных'),
            KeyboardButton(text='Создать новое упражнение'),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


# KeyboardButton('Внести_данные')
# KeyboardButton('Просмотр_данных')
# KeyboardButton('Создать_новое_упражнение')

# start_kb.add(save_data_exercises).add(get_data_exercises).add(save_name_exercises)



