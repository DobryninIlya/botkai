import random

from ..keyboards import exit
from .. import classes as command_class
from ..classes import vk, MessageSettings, UserParams, cursorR, conn


def info():
    msg = "Введите номер группы"
    msg_id = vk.method("messages.send",
                    {"peer_id": MessageSettings.id, "message": msg, "keyboard": exit, "random_id": random.randint(1, 2147483647)})
    cursorR.execute("INSERT INTO Status VALUES ({},{})".format(MessageSettings.getId(), 307))
    conn.commit()
    return "ok"





command = command_class.Command()




command.keys = ['бланк посещения', "журнал посещения"]
command.desciption = 'отображение полного списка группы'
command.process = info
command.payload = "prepod_blank"
command.role = [2]