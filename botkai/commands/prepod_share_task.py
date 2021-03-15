from .. import classes as command_class
from ..keyboards import exit
from ..classes import vk, MessageSettings, UserParams, conn, cursorR
import random
import datetime

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

command.keys = ['Отправить сообщение студентам']
command.description = 'связь со студентами'
command.process = info
command.payload = "prepod_share_task_next"
command.role = [2]
