import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import KeyboardProfile


async def info(MessageSettings, user):
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Управление рассылками происходит в профиле.",
                           keyboard=KeyboardProfile(MessageSettings, user),
                           random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = ["рассылки", "управление рассылками"]
command.desciption = ''
command.process = info
command.payload = "distr"
