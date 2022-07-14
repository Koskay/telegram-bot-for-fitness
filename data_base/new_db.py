from data_base.models import User, Category, Exercise, Progress
import datetime


category_list = ['Грудь', 'Спина', 'Ноги', 'Руки', 'Плечи']


async def load_categories():
    load_first_category = await Category.objects.exists()
    if not load_first_category:
        for cat in category_list:
            await Category.objects.create(category_name=cat)


async def get_categories():
    categories = await Category.objects.all()
    return categories


async def find_user(pk: int):
    user = await User.objects.get_or_none(id=pk)
    return user


async def add_user(user: dict):
    await User.objects.create(**user)


async def save_exercises_name(exercises: dict):
    await Exercise.objects.create(**exercises)


async def get_exercises(user_id: int, categories_id: int):
    exercises = await Exercise.objects.filter(user_id__id=user_id).filter(category_id__id=categories_id).all()
    return exercises


async def save_users_exercises(exercises_progress: dict):
    await Progress.objects.create(**exercises_progress)


async def get_progress(exercise: int, user_id: int):
    progress = await Progress.objects.select_related('exercise_id').filter(exercise_id=exercise, user_id=user_id).all()
    return progress


async def get_last_progress_user(exercise: int, user_id: int):
    date = await Progress.objects.filter(exercise_id=exercise, user_id=user_id).max('date')
    progress = await Progress.objects.select_related('exercise_id').filter(exercise_id=exercise, user_id=user_id, date=date).all()
    return progress


async def get_last_month_progress_user(exercise: int, user_id: int):
    max_date = await Progress.objects.filter(exercise_id=exercise, user_id=user_id).max('date')
    if max_date is not None:
        f_date = "%Y-%m-%d %H:%M:%S.%f"
        date = datetime.datetime.strptime(max_date, f_date) - datetime.timedelta(days=30)
        progress = await Progress.objects.select_related('exercise_id').filter(exercise_id=exercise, user_id=user_id, date__gte=date).all()
        return progress
    return []


async def update_user_weight(user: dict):
    await User.objects.filter(id=user['id']).update(weight=user['weight'])
