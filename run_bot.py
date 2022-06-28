from aiogram.utils import executor
from create_bot import dp
from data_base import db, new_db
from handlers import client, register, exercises_save, weight_update, save_exercises_name

categories = ['Грудь', 'Спина', 'Ноги', 'Руки', 'Плечи']


async def on_startup(_):
    print('bot is online')
    await new_db.new_sql_start()
    load_first_category = await new_db.Category.objects.exists()
    if not load_first_category:
        for cat in categories:
            await new_db.Category.objects.create(category_name=cat)
    # c = await new_db.Category.objects.all()
    # for e in c:
    #     print(e.category_name)
    # print(c)


client.register_handlers_client(dp)
register.register_handlers_register_client(dp)
exercises_save.register_handlers_save_progress(dp)
weight_update.register_handlers_update_weight(dp)
save_exercises_name.register_handlers_save_exercises_name(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
