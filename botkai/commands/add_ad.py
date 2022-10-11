import datetime
import random

from .. import classes as command_class
from ..keyboards import keyboardAddTasks
from ..classes import vk, MessageSettings, conn, cursorR


async def info():
    id = MessageSettings.getId()
    today = datetime.date.today()
    date = str(datetime.date(today.year, today.month, today.day) + datetime.timedelta(days=7))[5:]
    date = date.split('-')
    date = date[1] + "." + date[0]
    msg = 'Хочешь добавить Объявление? Такое объявление отображается вместе с расписанием в соответствующий день\n ' \
          'Введите число, на которое запланировано объявление. Например, "' + date + '". Важно ввести именно в таком формате (без кавычек).'
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=msg,
                           random_id=random.randint(1, 2147483647),
                           keyboard=keyboardAddTasks)

    sql = "INSERT INTO Status VALUES (" + str(id) + ", 52);"
    cursorR.execute(sql)
    conn.commit()
    return "ok"


command = command_class.Command()
command.keys = ['добавить объявление']
command.desciption = 'добавить объявление на определенный день'
command.process = info
command.payload = "add ad"
