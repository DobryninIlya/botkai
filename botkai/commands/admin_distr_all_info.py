from .. import classes as command_class
import random
from ..keyboards import make_admin_distr
from ..classes import vk, MessageSettings, conn, cursorR
import traceback

def info():

    vk.method("messages.send",
        {"peer_id": MessageSettings.id, "message": """Рассылка сообщения всем пользователям""","keyboard": make_admin_distr, "random_id": random.randint(1, 2147483647)})

    return "ok"





command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "admin_distr_all_info"
command.admlevel = 90