import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import activities_hub_event




async def info():
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Бот расписание занятий КНИТУ-КАИ",
                           random_id=random.randint(1, 2147483647),
                           keyboard=activities_hub_event)


info_command = command_class.Command()

info_command.keys = ['Творческое медиа-пространство КАИ']
info_command.desciption = 'Творческое медиа-пространство КАИ'
info_command.payload = "ACT_media"
info_command.process = info
