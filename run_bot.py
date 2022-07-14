from aiogram.utils import executor
from create_bot import dp, bot
from data_base import models, new_db
from handlers import client
from FSM import exercises_save, save_exercises_name, weight_update, register
from services import setting_commands


async def on_startup(_):
    print('bot is online')
    if await models.new_sql_start():
        await new_db.load_categories()
    await setting_commands.set_def_com(bot)


client.register_handlers_client(dp)
register.register_handlers_register_client(dp)
exercises_save.register_handlers_save_progress(dp)
weight_update.register_handlers_update_weight(dp)
save_exercises_name.register_handlers_save_exercises_name(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
