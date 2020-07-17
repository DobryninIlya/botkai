from .. import classes as command_class
from ..keyboards import keyboardTasks
from ..classes import vk, MessageSettings
import random


def info():
    id = MessageSettings.getPeer_id()
    vk.method("messages.send",
        {"peer_id": id, "message": 'Выберите пункт меню:', "keyboard" : keyboardTasks, "random_id": random.rndint(1, 2147483647)})

command = command_class.Command()

command.keys = ["задание", "задания"]
command.desciption = 'меню заданий'
command.process = info
command.payload = "task menu"
