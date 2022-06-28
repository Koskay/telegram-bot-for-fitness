import databases
import sqlalchemy
import ormar
import datetime


metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine('sqlite:///new_db.db')
database = databases.Database('sqlite:///new_db.db')


async def new_sql_start():
    metadata.create_all(engine)
    if not database.is_connected:
        await database.connect()


class User(ormar.Model):
    class Meta:
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True)
    username: str = ormar.String(max_length=150)
    weight: float = ormar.Float()


class Category(ormar.Model):
    class Meta:
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    category_name: str = ormar.String(max_length=150)


class Exercise(ormar.Model):
    class Meta:
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    exercise_name: str = ormar.String(max_length=150)
    user_id: int = ormar.ForeignKey(User)
    category_id: int = ormar.ForeignKey(Category)


class Progress(ormar.Model):
    class Meta:
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    weight: float = ormar.Float()
    repeats: int = ormar.Integer()
    date: datetime.datetime = datetime.datetime.now()
    user_id: int = ormar.ForeignKey(User)
    exercise_id: int = ormar.ForeignKey(Exercise)


async def get_categories():
    categories = await Category.objects.all()
    return categories


async def find_user(pk: int):
    user = await User.objects.get_or_none(id=pk)
    return user


async def add_user(user: dict):
    await User.objects.create(**user)


async def save_exercises_name(exercises: dict):
    print(**exercises)
    await Exercise.objects.create(**exercises)


async def get_exercises(user_id: int, categories_id: int):
    exercises = await Exercise.objects.filter(user_id__id=user_id).filter(category_id__id=categories_id).all()
    return exercises


async def save_users_exercises(exercises_progress: dict):
    await Progress.objects.create(**exercises_progress)


async def get_progress(exercise: int, user_id: int):
    progress = await Progress.objects.filter(exercise_id=exercise, user_id=user_id).all()
    return progress


async def get_last_progress_user(exercise: int, user_id: int):
    pass