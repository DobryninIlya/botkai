import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import make_warn


async def info(MessageSettings, user):
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="""Предупреждения - это наказание за определенные нарушения правил. 
        Обычно они выдаются за различные оскорбления и нецензурные выражения при создании заданий, объявлений, смене ника и т.д.
        Если на аккаунте активны 3 предупреждения, то доступ к сервису ограничивается.""",
                           random_id=random.randint(1, 2147483647),
                           keyboard=make_warn)
    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "starosta_warn_info"
command.admlevel = 2
