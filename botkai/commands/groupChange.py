import random
import traceback

from .. import classes as command_class
from ..classes import vk, conn, cursorR
from ..keyboards import keyboardAddTasks2


async def info(MessageSettings, user):
    id = MessageSettings.getId()

    try:
        sql = "INSERT INTO Status VALUES (" + str(id) + ", 56);"
        cursorR.execute(sql)
        conn.commit()
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Введи группу в чат",
                               random_id=random.randint(1, 2147483647),
                               keyboard=keyboardAddTasks2)
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        conn.rollback()
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Произошла ошибка. Повторите позже",
                               random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = ['!группа', "группа"]
command.desciption = 'изменение группы'
command.process = info
command.payload = "groupchange"