from .. import classes as command_class
from ..keyboards import keyboardPrepodShareTask
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random
import datetime

uptime = datetime.datetime.now()


def info():
    vk.method("messages.send",
              {"peer_id": MessageSettings.getId(), "message": "Вы можете создать и отправить задание студентам.",
               "keyboard": keyboardPrepodShareTask, "random_id": random.randint(1, 2147483647)})

    return "ok"


command = command_class.Command()

command.keys = ['Создать задание студентам справка']
command.description = 'задание студентам справка'
command.process = info
command.payload = "prepod_share_task_info"
command.role = [2]
