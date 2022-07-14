import databases
import sqlalchemy
import ormar
from datetime import datetime


metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine('sqlite:///new_db.db')
database = databases.Database('sqlite:///new_db.db')


async def new_sql_start():
    metadata.create_all(engine)
    if not database.is_connected:
        await database.connect()
    return database.is_connected


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
    date: datetime = ormar.DateTime(default=datetime.now())
    user_id: int = ormar.ForeignKey(User)
    exercise_id: int = ormar.ForeignKey(Exercise)