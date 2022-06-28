from typing import Union
from aiogram import types, Dispatcher
from handlers import other, exercises_save , save_exercises_name
from create_bot import dp
from data_base import db, new_db
from keyboards import kb_client, client_kb, start_kb, inline_kb
from keyboards.inline_kb import menu_cd


#@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    """Команда старт"""
    user = await new_db.find_user(message.from_user.id)
    if user is not None:
        await message.answer(f'Здравствуйте, {message.from_user.full_name}\n'
                             f'Ваш вес {user.weight}', reply_markup=start_kb)
    else:
        await message.answer('Зарегистрируйтесь')


# '''Получение данных по категориям'''
#
#
# async def command_get_categories(message: types.Message):
#     await client_kb.categories()
#     await message.answer('Выберите категорию', reply_markup=kb_client)
#
#
# '''Получение данных по категориям'''
#
#
# async def command_put_categories(message: types.Message):
#     await client_kb.categories()
#     await message.answer('Выберите категорию', reply_markup=kb_client)


# async def load_progresss(message: types.Message):
#     us_id = int(message.from_user.id)
#     progress = await db.select_progress(message.text.strip('/'), us_id)
#     progress_user = other.parse(progress)
#     await message.answer(progress_user)


'''Инлайн кнопки с категориями'''


async def get_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    if str(message.get_command()) == '/Внести_данные':
        save = 'save_data'
    elif str(message.get_command()) == '/Создать_новое_упражнение':
        save = 'save_name'
    else:
        save = 'get'
    markup = await inline_kb.categories_kb(save)
    await message.answer('Выберите категорию', reply_markup=markup)


'''Инлайн кнопки с упражнениями'''


async def get_sub_categories(callback: types.CallbackQuery, categories: int, save: str, **kwargs):
    user_id = callback.from_user.id
    markup = await inline_kb.sub_categories_kb(categories, save, user_id)
    if not markup:
        await callback.message.answer('У вас пока нет записей')
    else:
        await callback.message.edit_reply_markup(markup)
        await callback.answer('Выберите упражнение')


async def get_variable_sub_categories(callback: types.CallbackQuery, categories: int, save: str,
                                      exercises: int, **kwargs):
    markup = await inline_kb.variable_sub_categories_kb(categories, save, exercises)
    await callback.message.edit_reply_markup(markup)


'''Выводит прогресс пользователя'''


async def load_progress(callback: types.CallbackQuery, variable: str, exercises: int, **kwargs):
    us_id = int(callback.from_user.id)
    if variable == 'Последние результаты':
        progress = await new_db.get_last_progress_user(exercises, us_id)
    elif variable == 'Прогресс за месяц':
        progress = await db.get_progress_user_month(exercises, us_id)
    else:
        progress = await new_db.get_progress(exercises, us_id)
    progress_user = other.parse(progress)
    await callback.message.answer(progress_user)


# '''Выводит последний введенный прогресс пользователя'''
#
#
# async def last_progress_user(callback: types.CallbackQuery, categories, exercises, **kwargs):
#     us_id = int(callback.from_user.id)
#     progress = await db.get_progress_user_last(exercises, us_id)
#     progress_user = other.parse(progress)
#     await callback.message.answer(progress_user)
#
#
# '''Выводит прогресс пользователя за последний месяц'''
#
#
# async def month_progress_user(callback: types.CallbackQuery, categories, exercises, **kwargs):
#     us_id = int(callback.from_user.id)
#     progress = await db.get_progress_user_last(exercises, us_id)
#     progress_user = other.parse(progress)
#     await callback.message.answer(progress_user)


"""При нажатии на инлайн кнопку запускаем нужную функцию"""


@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: types.CallbackQuery, callback_data: dict):
    curr_level = callback_data.get('level')
    category = callback_data.get('category')
    sub_category = callback_data.get('exercises')
    use_id = callback_data.get('user_id')
    save = callback_data.get('save')
    variable = callback_data.get('variable')

    # создаем словарь с уровнем вложенности инлайн кнопок и вызываем соотв. функцию
    levels = {
        '1': get_sub_categories,
        '2': get_variable_sub_categories,
        '3': load_progress,
    }

    # флаг save, при котором меням функцию вывода прогресса, на ввод
    if save == 'save_data':
        levels['2'] = exercises_save.cm_start_save
        del levels['3']
    elif save == 'save_name':
        levels['1'] = save_exercises_name.cm_start_save_name
        del levels['2']
        del levels['3']

    curr_level_func = levels[curr_level]
    await curr_level_func(
        call,
        categories=category,
        exercises=sub_category,
        user_id=use_id,
        variable=variable,
        save=save
    )


'''Регистрация хендлеров'''


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    dp.register_message_handler(get_categories, commands=['Просмотр_данных', 'Внести_данные',
                                                          'Создать_новое_упражнение'])
    # dp.register_message_handler(get_categories, commands='Внести_данные')
    #dp.register_message_handler(command_get_categories, commands=['Просмотр_данных',])
    #dp.register_message_handler(load_progress, commands=['Грудь', 'Ноги', 'Спина', 'Плечи', 'Руки'])



