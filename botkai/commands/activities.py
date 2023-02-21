import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import activities_hub


async def info(MessageSettings, user):
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Студенческие организации и самоуправления\n Глава такого объединения? Напиши мне ( @ilya_dobrynin ), чтобы оказаться здесь и о тебе узнали люди",
                           random_id=random.randint(1, 2147483647),
                           keyboard=activities_hub)

info_command = command_class.Command()

info_command.keys = ['активности']
info_command.desciption = ''
info_command.payload = "activities"
info_command.process = info
