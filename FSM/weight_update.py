from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from data_base import  new_db
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMUpdateClient(StatesGroup):
    weight = State()


'''Начало регистрации пользователя'''


async def cm_weight_user(message: types.Message):
    await FSMUpdateClient.weight.set()
    await message.reply('Введите вес')


async def load_weight_user(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = float(message.text)
        data['id'] = message.from_user.id
    await new_db.update_user_weight(data)
    await state.finish()


'''Регистрация хендлеров'''


def register_handlers_update_weight(dp: Dispatcher):
    dp.register_message_handler(cm_weight_user, commands='Вес', state=None)
    dp.register_message_handler(load_weight_user, state=FSMUpdateClient.weight)