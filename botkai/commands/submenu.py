import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import submenu


async def info(MessageSettings, user):
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Меню",
                           random_id=random.randint(1, 2147483647),
                           keyboard=submenu)


info_command = command_class.Command()

info_command.keys = ['разное', 'дополнительное меню']
info_command.desciption = 'доп меню'
info_command.payload = "submenu"
info_command.process = info
