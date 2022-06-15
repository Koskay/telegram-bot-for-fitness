from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from data_base import db
from aiogram.dispatcher.filters.state import State, StatesGroup
import time


class FSMClientExercisesNameSave(StatesGroup):
    name = State()


'''Начало состояния сохранения прогресса'''


async def cm_start_save_name(callback: types.CallbackQuery, categories, **kwargs,):
    global categories_id
    categories_id = categories
    await FSMClientExercisesNameSave.name.set()
    await callback.message.answer('Введите название упражнения')


'''Отмена сохранения в бд'''


#@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.delete()
    await message.answer('Сохранение отменино')
    await message.answer('Обращайся')


'''Ловим кол-во повторов'''


#@dp.message_handler(state=FSMClient.weight)
async def load_name_exercises(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
        data['cat_id'] = categories_id
        data['name'] = message.text
    await db.save_exercises_name(state)
    await state.finish()
    await message.answer('Успешно!')


'''Регистрация хендлеров'''


def register_handlers_save_exercises_name(dp: Dispatcher):
    dp.register_message_handler(cancel_state, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_name_exercises, state=FSMClientExercisesNameSave.name)