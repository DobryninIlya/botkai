import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import activities_hub



async def info(MessageSettings, user):
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="В данном разделе временно нет данных.",
                           random_id=random.randint(1, 2147483647))


info_command = command_class.Command()

info_command.keys = []
info_command.desciption = ''
info_command.payload = "ACT_notaviable"
info_command.process = info
