from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from data_base import db

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
start_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)


save_data_exercises = KeyboardButton('/Внести_данные')
get_data_exercises = KeyboardButton('/Просмотр_данных')
save_name_exercises = KeyboardButton('/Создать_новое_упражнение')

start_kb.add(save_data_exercises).add(get_data_exercises).add(save_name_exercises)



