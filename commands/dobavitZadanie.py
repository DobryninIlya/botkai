import datetime
import random

from .. import classes as command_class
from ..classes import vk, conn, cursorR
from ..keyboards import keyboardAddTasks


async def info(MessageSettings, user):
    today = datetime.date.today()
    id = MessageSettings.getId()
    date = str(datetime.date(today.year, today.month, today.day)  + datetime.timedelta(days=7))[5:]
    date = date.split('-')
    date = date[1] + "." + date[0]
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message='Хочешь добавить задание? Такое задание видят все участники группы. \n Введите число, на которое запланировано задание. Например, "' + date + '". Важно ввести именно в таком формате (без кавычек).',
                           keyboard=keyboardAddTasks,
                           random_id=random.randint(1, 2147483647))
    sql = "INSERT INTO Status VALUES (" + str(id) + ", 50);"
    cursorR.execute(sql)
    conn.commit()
    return "ok"

command = command_class.Command()

command.keys = ['добавить задание']
command.desciption = 'добавить задание на определенный день'
command.process = info
command.payload = "add task"