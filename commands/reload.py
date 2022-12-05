import random
import sys

from .. import classes as command_class
from ..classes import vk


async def info(MessageSettings, user):
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Перезагрузка...",
                           random_id=random.randint(1, 2147483647))
    sys.exit(1)

    return "ok"


command = command_class.Command()

command.keys = ['reload']
command.desciption = 'рестарт'
command.process = info
command.payload = "reload"
command.admlevel = 90
