import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import activities_hub


async def info():
    msg = """Тренировка в КАИ!
Где? Карла Маркса, 31 (5 здание)
Когда? Среда, 18:30
Аудитория? 318
Что? Дебаты!
Подробнее: @debateclubkai"""
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=msg,
                           random_id=random.randint(1, 2147483647))


info_command = command_class.Command()

info_command.keys = ['информация клуб дебатов']
info_command.desciption = ''
info_command.payload = "ACT_media_debati_info_kai"
info_command.process = info
