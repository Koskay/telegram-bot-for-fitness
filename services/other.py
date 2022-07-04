import datetime


# функция переволить данные из бд в нормальный вид
def parse(progress_list: list):
    if progress_list:
        format_string = [f'____________\nКол-во повторов: {pr.repeats} \nВес: {pr.weight} kg\nДата: {date_format(pr.date)}\n' for pr in
                         progress_list]
        return f'{progress_list[0].exercise_id.exercise_name}\n' + ''.join(format_string)
    else:
        return 'У вас пока нет записей'


def date_format(date: datetime.datetime):
    if not date:
        return ''
    date_now = date.strftime('%d-%m-%Y')
    return date_now


msg = []  # список для хранения callback сообщения от бота


async def update_chat_message(callback_message):
    if msg:  # если в списке есть сообщения то мы его удаляем из чата и из списка
        await msg[0].delete()
        msg.pop()
    msg.append(callback_message)
