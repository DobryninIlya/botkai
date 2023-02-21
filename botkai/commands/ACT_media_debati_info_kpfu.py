import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import activities_hub


async def info(MessageSettings, user):
    msg = """Тренировка в КФУ!
Где? Бутлерова, 4
Когда? Четверг, 18:30
Аудитория? В306
Что? Дебаты!
Подробнее: @kfu_debate"""
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=msg,
                           random_id=random.randint(1, 2147483647))


info_command = command_class.Command()

info_command.keys = ['информация клуб дебатов']
info_command.desciption = ''
info_command.payload = "ACT_media_debati_info_kpfu"
info_command.process = info
