import datetime
import random

from .. import classes as command_class
from ..classes import vk, MessageSettings, conn, cursorR
from ..keyboards import exit

uptime = datetime.datetime.now()


def info():
    vk.method("messages.send",
              {"peer_id": MessageSettings.getId(), "message": "Введите номер группы, студентам которой "
                                                              "будет разослано задание",
               "keyboard": exit, "random_id": random.randint(1, 2147483647)})
    cursorR.execute("INSERT INTO Status VALUES ({},{})".format(MessageSettings.getId(), 304))
    conn.commit()

    return "ok"


command = command_class.Command()

command.keys = ['Отправить задание студентам']
command.description = 'задание студентам'
command.process = info
command.payload = "prepod_share_task_next"
command.role = [2]
