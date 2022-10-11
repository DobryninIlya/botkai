import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import week_shed_kbrd


async def info():
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Меню",
                           keyboard=week_shed_kbrd,
                           random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "week_shed_menu"
command.role = [1, 2, 3, 6]
