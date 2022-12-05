import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import getMainKeyboard


async def info(MessageSettings, user):
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Обновлено",
                           keyboard=getMainKeyboard(user.role),
                           random_id=random.randint(1, 2147483647))


info_command = command_class.Command()

info_command.keys = ['обновить', 'обновление']
info_command.desciption = 'получение обновления'
info_command.payload = "getupdate"
info_command.process = info
info_command.role = [1, 2, 3, 4, 5, 6]
