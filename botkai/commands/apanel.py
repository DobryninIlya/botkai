from .. import classes as command_class
import random
from ..keyboards import GetAdminPanel
from ..classes import vk, MessageSettings, UserParams


async def info():
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Apanel",
                           random_id=random.randint(1, 2147483647),
                           keyboard=GetAdminPanel(UserParams.getAdminLevel()))
    return "ok"


command = command_class.Command()
command.keys = ['apanel']
command.desciption = 'админ панель'
command.process = info
command.payload = "apanel"
command.admlevel = 4
command.role.append(2)
