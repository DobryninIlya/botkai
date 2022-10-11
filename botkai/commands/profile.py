import random

from .. import classes as command_class
from ..classes import MessageSettings
from ..classes import vk as vk
from ..keyboards import KeyboardProfile


async def info():
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Профиль",
                           keyboard=KeyboardProfile(),
                           random_id=random.randint(1, 2147483647))


command = command_class.Command()

command.keys = ['профиль', 'настройки']
command.desciption = 'Покажу твой профиль'
command.process = info
command.payload = "profile"
command.role = [1,3,6]