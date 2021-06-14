import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import make_warn


def info():

    vk.method("messages.send",
        {"peer_id": MessageSettings.id, "message": """Предупреждения - это наказание за определенные нарушения правил. 
        Обычно они выдаются за различные оскорбления и нецензурные выражения при создании заданий, объявлений, смене ника и т.д.
        Если на аккаунте активны 3 предупреждения, то доступ к сервису ограничивается.""","keyboard": make_warn, "random_id": random.randint(1, 2147483647)})

    return "ok"





command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "starosta_warn_info"
command.admlevel = 2