import random
import traceback

from .. import classes as command_class
from ..classes import vk, MessageSettings, conn, cursorR
from ..keyboards import keyboardAddTasks2


def info():
    id = MessageSettings.getId()

    try:
        sql = "INSERT INTO Status VALUES (" + str(id) + ", 56);"
        cursorR.execute(sql)
        conn.commit()
        vk.method("messages.send",
            {"peer_id": id, "message": "Введи группу в чат", "keyboard": keyboardAddTasks2, "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        conn.rollback()
        vk.method("messages.send",
            {"peer_id": id, "message": "Произошла ошибка. Повторите позже", "random_id": random.randint(1, 2147483647)})

    return "ok"


command = command_class.Command()

command.keys = ['!группа', "группа"]
command.desciption = 'изменение группы'
command.process = info
command.payload = "groupchange"