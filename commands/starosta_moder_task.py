import random

from .. import classes as command_class
from ..classes import vk, cursor
from ..keyboards import GetModerTaskStarosta


async def info(MessageSettings, user):
    UserID = MessageSettings.getId()
    if "callback" not in MessageSettings.buttons:
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Команда доступна только в мобильной версии сайта m.vk.com и в последней версии официального мобильного приложения.",
                               random_id=random.randint(1, 2147483647))
        return
    groupId = user.getGroup()
    sql = "SELECT * FROM Task WHERE" + " groupid = " + str(groupId) + " LIMIT 2"
    cursor.execute(sql)
    task = ""
    att = ""

    curs = cursor.fetchall()
    # print(curs)
    if len(curs) == 0:
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Заданий не создано",
                               random_id=random.randint(1, 2147483647))
        return "ok"
    first = True
    next_task_id = -1
    for row in curs:
        if first:
            task = "❗зᴀдᴀниᴇ❗\n"
            task += str(row[4])
            idvk = "@id" + str(row[2])
            task += "\n" + idvk + " (Автор) | ID: " + str(row[0])
            att = str(row[5])
            first = False
        else:
            next_task_id = int(row[0])

    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=task,
                           content_source=row[7],
                           keyboard=GetModerTaskStarosta(id=int(row[0]), next_id=next_task_id, pos_id=0, prev_id=0),
                           attachment=att,
                           random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = ['проверка заданий']
command.desciption = ''
command.process = info
command.payload = "starostatask"
command.admlevel = 2
