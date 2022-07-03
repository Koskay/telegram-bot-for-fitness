import datetime


# функция переволить данные из бд в нормальный вид
def parse(progress_list: list):
    if progress_list:
        format_string = [f'Кол-во повторов: {pr.repeats} \nВес: {pr.weight} kg\nДата: {date_format(pr.date)} \n' for pr in
                         progress_list]
        return ''.join(format_string)
    else:
        return 'У вас пока нет записей'


def date_format(date: datetime.datetime):
    if not date:
        return ''
    date_now = date.strftime('%d-%m-%Y')
    return date_now
