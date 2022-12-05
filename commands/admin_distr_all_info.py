import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import make_admin_distr


async def info(MessageSettings, user):
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Рассылка сообщения всем пользователям",
                           random_id=random.randint(1, 2147483647),
                           keyboard=make_admin_distr)
    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "admin_distr_all_info"
command.admlevel = 90
