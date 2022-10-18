import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import buildings_menu


async def info(MessageSettings, user):
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Выберите здание",
                           random_id=random.randint(1, 2147483647),
                           keyboard=buildings_menu)
    return "ok"


info_command = command_class.Command()

info_command.keys = ['здания']
info_command.desciption = 'меню команд "разное"'
info_command.payload = "buildings_menu"
info_command.process = info
