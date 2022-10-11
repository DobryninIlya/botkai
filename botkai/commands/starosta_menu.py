import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import GetStarostaKeyboard


async def info():
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Меню старосты",
                           keyboard=GetStarostaKeyboard(),
                           random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "starosta_menu"
command.admlevel = 2
