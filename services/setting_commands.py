from aiogram.types import BotCommand
from create_bot import bot


async def set_def_com(bot: bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand('/menu', 'показываеть меню'),
            BotCommand('/weight_update', 'изменить вес'),
            BotCommand('/register', 'регистрация'),
            BotCommand('/help', 'Описание функций бота'),
        ]
    )
