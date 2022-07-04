from typing import Union
from aiogram import types, Dispatcher
from services import other
from FSM import exercises_save, save_exercises_name
from create_bot import dp
from data_base import new_db
from keyboards import inline_kb
from keyboards.inline_kb import menu_cd


"""Команда старт"""


async def command_start(message: types.Message):
    user = await new_db.find_user(message.from_user.id)
    if user is not None:
        markup = await inline_kb.start_choice()
        await message.answer(f'Здравствуйте, {message.from_user.full_name}\n'
                             f'Ваш вес {user.weight}', reply_markup=markup)
    else:
        await message.answer('Зарегистрируйтесь')


async def choice(message: Union[types.Message, types.CallbackQuery], **kwargs):
    markup = await inline_kb.choice_of_actions()
    await message.message.edit_reply_markup(markup)
    await message.answer()

'''Инлайн кнопки с категориями'''


async def get_categories(message: Union[types.Message, types.CallbackQuery], **kwargs):
    if kwargs['save'] == 'save_p':
        save = 'save_data'
    elif kwargs['save'] == 'save_exercise':
        save = 'save_name'
    else:
        save = 'get'
    markup = await inline_kb.categories_kb(save)
    await message.message.edit_reply_markup(markup)
    await message.answer('Выберите категорию')


'''Инлайн кнопки с упражнениями'''


async def get_sub_categories(callback: types.CallbackQuery, categories: int, save: str, **kwargs):
    user_id = callback.from_user.id
    markup = await inline_kb.sub_categories_kb(categories, save, user_id)
    if not markup:
        await callback.answer('У вас пока нет записей')
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
        progress = await new_db.get_last_month_progress_user(exercises, us_id)
    else:
        progress = await new_db.get_progress(exercises, us_id)
    progress_user = other.parse(progress)
    callback_message = await callback.message.answer(progress_user)  # сохраняем ответ бота в переменную
    await other.update_chat_message(callback_message)
    await callback.answer()


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
        '0': choice,
        '1': get_categories,
        '2': get_sub_categories,
        '3': get_variable_sub_categories,
        '4': load_progress,
    }

    # флаг save, при котором меням функцию вывода прогресса, на ввод
    if save == 'save_data':
        levels['3'] = exercises_save.cm_start_save
        del levels['4']
    elif save == 'save_name':
        levels['2'] = save_exercises_name.cm_start_save_name
        del levels['3']
        del levels['4']

    curr_level_func = levels[curr_level]
    await curr_level_func(
        call,
        categories=category,
        exercises=sub_category,
        user_id=use_id,
        variable=variable,
        save=save,
    )


'''Регистрация хендлеров'''


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands='start')
    # dp.register_message_handler(get_categories, Text(equals=['Просмотр данных', 'Внести данные',
    #                                                          'Создать новое упражнение']))





