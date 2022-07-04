from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from data_base import new_db


menu_cd = CallbackData('show_result', 'level', 'category', 'exercises', 'user_id', 'save', 'variable')


# функция устанавливает параметры по умолчанию, если они не были переданы
def make_callback_data(level=0, user_id=0, category=0, exercises=0, save='get', variable=''):
    return menu_cd.new(level=level, user_id=user_id, category=category, exercises=exercises,
                       save=save, variable=variable)


async def start_choice():
    choice = 'Начать'
    markup = InlineKeyboardMarkup()

    data = make_callback_data()
    markup.insert(
        InlineKeyboardButton(text=choice, callback_data=data)
    )
    return markup


async def choice_of_actions():
    curr_level = 0
    choice_dict = {'get': 'Просмотр данных', 'save_p': 'Внести данные', 'save_exercise': 'Создать новое упражнение'}
    markup = InlineKeyboardMarkup(row_width=1)
    for var, text in choice_dict.items():
        data = make_callback_data(save=var, level=curr_level+1)
        markup.insert(
            InlineKeyboardButton(text=text, callback_data=data)
        )
    return markup


# формуриюет инлайн кнопки первого уровня с категориями
async def categories_kb(save: str):
    curr_level = 1
    markup = InlineKeyboardMarkup()

    categories = await new_db.get_categories()
    for category in categories:
        butt_text = f'{category.category_name}'
        data = make_callback_data(level=curr_level+1, category=category.id, save=save)

        markup.insert(
            InlineKeyboardButton(text=butt_text, callback_data=data)
        )

    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=curr_level - 1,
                                             )
        )
    )

    return markup


# формуриюет инлайн кнопки второго уровня с упражнениями
async def sub_categories_kb(categories_id: int, save: str, user_id: int):
    sub_categories = await new_db.get_exercises(user_id, int(categories_id))
    if not sub_categories:
        markup = False
        return markup
    curr_level = 2
    markup = InlineKeyboardMarkup(row_width=1)
    for exercise in sub_categories:
        butt_text = f'{exercise.exercise_name}'
        data = make_callback_data(level=curr_level+1, category=exercise.category_id.id,
                                  exercises=exercise.id, save=save)

        markup.insert(
            InlineKeyboardButton(text=butt_text, callback_data=data)
        )

    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=curr_level - 1, category=categories_id,
                                             save=save)
        )
    )

    return markup


# инлайн кнопки 3 уровня с вариантами вывода
async def variable_sub_categories_kb(categories_id: int, save: str, exercises_id: int):
    curr_level = 3
    markup = InlineKeyboardMarkup(row_width=1)

    butt_text = ['Прогресс за месяц', 'Последние результаты', 'Пргоресс за все время']
    for text in butt_text:
        data = make_callback_data(level=curr_level+1, category=categories_id, save=save,
                                  exercises=exercises_id, variable=text)

        markup.insert(
            InlineKeyboardButton(text=text, callback_data=data)
        )

    markup.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=make_callback_data(level=curr_level - 1, category=categories_id,
                                             exercises=exercises_id, save=save)
        )
    )

    return markup
