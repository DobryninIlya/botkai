import json
import random

from .. import classes as command_class
from ..classes import vk, cursor
from ..keyboards import get_button


async def info(MessageSettings, user):
    sql = "SELECT potok_lecture FROM users WHERE id_vk = {id_vk}".format(id_vk=MessageSettings.getId())
    cursor.execute(sql)
    res = cursor.fetchone()[0]

    if res:
        cursor.execute("UPDATE users SET potok_lecture = {} WHERE ID_VK = {}".format(False, MessageSettings.getId()))
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Отображение потоковых лекций выключено",
                               random_id=random.randint(1, 2147483647))

    else:
        cursor.execute("UPDATE users SET potok_lecture = {} WHERE ID_VK = {}".format(True, MessageSettings.getId()))
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Отображение потоковых лекций включено",
                               random_id=random.randint(1, 2147483647))
    return "ok"


command = command_class.Command()

command.keys = ["поток", "потоковая лекция"]
command.desciption = 'включить или отключить отображение дистанционных лекций'
command.process = info
command.payload = "potokLectureSettings"
