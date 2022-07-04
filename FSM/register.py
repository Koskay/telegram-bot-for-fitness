from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from data_base import new_db
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import inline_kb


class FSMClient(StatesGroup):
    name = State()
    weight = State()


'''Начало регистрации пользователя'''


async def cm_start(message: types.Message):
    user = await new_db.find_user(message.from_user.id)
    if user:
        await message.answer('Вы уже зарегистрированы')
    else:
        await FSMClient.name.set()
        await message.reply('Введите имя')


'''Отмена регистрации'''


async def cancel_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.delete()
    await message.answer('Регистрация отменина')
    await message.answer('Обращайся')


'''Ловим имя пользователя'''


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.from_user.id
        data['username'] = message.text
        await FSMClient.next()
        await message.reply('Введите ваш текущий вес')


'''Ловим вес пользователя'''


async def load_weight(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        async with state.proxy() as data:
            data['weight'] = float(message.text)
        await new_db.add_user(data)
        await state.finish()
        markup = await inline_kb.start_choice()
        await message.answer(f'Здравствуйте, {message.from_user.full_name}\n',
                             reply_markup=markup)
    else:
        await message.answer('Введите число\n'
                             'Или напишите <отмена>, что бы отменить сохранение')


'''Регистрация хендлеров'''


def register_handlers_register_client(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands='Регистрация', state=None)
    dp.register_message_handler(cancel_state, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(load_name, state=FSMClient.name)
    dp.register_message_handler(load_weight, state=FSMClient.weight)