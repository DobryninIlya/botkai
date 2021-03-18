import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import make_distr


def info():

    vk.method("messages.send",
        {"peer_id": MessageSettings.id, "message": """Ты можешь разослать любое сообщение всей своей группе. Внимание, сообщение показывается ВСЕМ участникам группы.""","keyboard": make_distr, "random_id": random.randint(1, 2147483647)})

    return "ok"





command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "starosta_distr_info"
command.admlevel = 2