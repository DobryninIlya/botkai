import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import make_kick


async def info(MessageSettings, user):
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Вы можете кикнуть человека из группы, если он вам мешает.",
                           keyboard=make_kick,
                           random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "starosta_kick_info"
command.admlevel = 2
