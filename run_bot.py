from aiogram.utils import executor
from create_bot import dp
from data_base import models
from handlers import client
from FSM import exercises_save, save_exercises_name, weight_update, register

categories = ['Грудь', 'Спина', 'Ноги', 'Руки', 'Плечи']


async def on_startup(_):
    print('bot is online')
    await models.new_sql_start()
    load_first_category = await models.Category.objects.exists()
    if not load_first_category:
        for cat in categories:
            await models.Category.objects.create(category_name=cat)


client.register_handlers_client(dp)
register.register_handlers_register_client(dp)
exercises_save.register_handlers_save_progress(dp)
weight_update.register_handlers_update_weight(dp)
save_exercises_name.register_handlers_save_exercises_name(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
