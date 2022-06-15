import sqlite3 as sq


categories = ('Грудь', 'Спина', 'Ноги', 'Руки', 'Плечи')


# установка соединения с бд
def sql_start():
    global base, curs
    base = sq.connect('fitne_base.sqlite3')
    curs = base.cursor()
    if base:
        print('connect to base')
    base.execute('CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, weight REAL)')
    base.execute('CREATE TABLE IF NOT EXISTS categories(name TEXT, id INTEGER PRIMARY KEY)')
    base.execute('CREATE TABLE IF NOT EXISTS exercises(user_id INTEGER,'
                 'cat_id INTEGER, name TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT)')
    base.execute('CREATE TABLE IF NOT EXISTS user_progress(use_id INTEGER, exerc_id INTEGER, weight REAL, '
                 'repeats INTEGER, date TEXT)')
    category = curs.execute('SELECT * FROM categories').fetchall()
    if not category:
        for i, cat in enumerate(categories, 1):
            curs.execute('INSERT INTO categories VALUES (?, ?)', (cat, i))
    base.commit()


# Создание упражнений
async def save_exercises_name(state):
    async with state.proxy() as data:
        print(data)
        curs.execute('INSERT INTO exercises (user_id, cat_id, name) VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()


# добовляет пользователя в бд
async def add_user(state):
    async with state.proxy() as data:
        curs.execute('INSERT INTO users VALUES (?, ?, ?)', tuple(data.values()))
        base.commit()


# обновляет вес пользователя
async def update_user_weight(state):
    async with state.proxy() as data:
        print(data)
        curs.execute('UPDATE users SET weight = ? WHERE id = ?', tuple(data.values()))
        base.commit()


# сохроняеи прогресс пользователя
async def save_users_exercises(state):
    async with state.proxy() as data:
        curs.execute('INSERT INTO user_progress VALUES (?, ?, ?, ?, ?)', tuple(data.values()))
        base.commit()


# проверят наличие пользователя в бд
async def find_user(user_id):
    user = curs.execute('SELECT * FROM users WHERE id={}'.format(user_id)).fetchone()
    if user is not None:
        print(user)
        return user


# получает все категории
async def get_categories():
    categories = curs.execute('SELECT * FROM categories').fetchall()
    return categories


# получает все упражения заданной категории
async def get_sub_categories(cat_id, user_id):
    sub_categories = curs.execute('SELECT * FROM exercises WHERE cat_id = ? and user_id = ?', (cat_id, user_id))
    return sub_categories


# async def select_progress(cat, us_id):
#     progress = curs.execute('select weight, repeats, exercises.name  from user_progress join exercises on exerc_id == exercises.id join categorys on exercises.cat_id == categorys.cat_id where categorys.name == "{}" and user_progress.use_id == {}'.format(cat, us_id)).fetchall()
#     return progress

# получает прогресс конкретного пользователя
async def get_progress(exercises_id, user_id):
    progress = curs.execute(
        'select weight, repeats, date from user_progress where exerc_id = ? and user_progress.use_id = ?',
        (exercises_id, user_id)).fetchall()
    return progress


# получает последнюю запись пользователя
async def get_progress_user_last(exercises_id, user_id):
    progress = curs.execute(
        'select weight, repeats, max(date) from user_progress where exerc_id = ? and user_progress.use_id = ?',
        (exercises_id, user_id)).fetchone()
    return progress


# получает записи за последний месяц
async def get_progress_user_month(exercises_id, user_id):
    progress = curs.execute(
        'select weight, repeats, date from user_progress where exerc_id = ? and user_progress.use_id = ? and '
        'date > (select max(date) from user_progress where exerc_id = ? and use_id = ? ) - 2629743',
        (exercises_id, user_id, exercises_id, user_id)).fetchall()
    return progress
