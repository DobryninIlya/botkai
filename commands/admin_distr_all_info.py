import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import make_admin_distr


def info():
    vk.method("messages.send",
              {"peer_id": MessageSettings.id, "message": """Рассылка сообщения всем пользователям""",
               "keyboard": make_admin_distr, "random_id": random.randint(1, 2147483647)})

    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "admin_distr_all_info"
command.admlevel = 90
