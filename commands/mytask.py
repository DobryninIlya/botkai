import random

from .. import classes as command_class
from ..classes import vk, cursor
from ..keyboards import GetDeleteTaskButton, keyboardTasks


async def info(MessageSettings, user):
    UserID = MessageSettings.getId()
    sql = "SELECT * FROM Task WHERE" + " UserID = " + str(UserID)
    cursor.execute(sql)
    task = ""
    att = ""

    curs = cursor.fetchall()
    if len(curs) == 0:
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Заданий нет. Самое время добавить!",
                               keyboard=keyboardTasks,
                               random_id=random.randint(1, 2147483647))

    for row in curs:
        task = "❗зᴀдᴀниᴇ❗\n"
        task += str(row[4])
        idvk = "@id" + str(row[2])
        task += "\n" + idvk + " (Автор) | ID: " + str(row[0])
        att = str(row[5])
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message=task,
                               keyboard=GetDeleteTaskButton((int)(row[0])),
                               attachment=att,
                               random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = ['мои задания', 'мои задачи']
command.desciption = 'отображение списка заданий'
command.process = info
command.payload = "mytask"
command.role = [1, 2, 3, 6]
