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


message_fo_command_help = 'Бот служит для записи и учета вашего физического прогресса\n\n' \
                  'Для начала вы должны зарегистрироваться /register\n\n' \
                  'Вы можете открыть меню командой /menu\n' \
                  'При выборе:\n' \
                  '"Создать новое упражнение" - вы можете выбрать категорию и ' \
                  'создать любое упражнение\n\n' \
                  '"Сохранить результаты" - вы сохраняете ваши результаты ' \
                  'по конкретному упражнению(кол. повторов и вес отягощения)\n\n' \
                  '"Просмотр результатов" - просмотр ваших результатов ' \
                  'по конкретному упражнению в удобном вам формате\n\n' \
                  '/weight_update - обновление вашего веса, для наглядного отслеживания вашего прогресса'
