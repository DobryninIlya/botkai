import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import verification


async def info():
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Верификация аккаунта необходима для подтверждения того, что вы являетесь студентом. Некоторые функции могут быть недоступны неверефицированным пользователям.",
                           random_id=random.randint(1, 2147483647),
                           keyboard=verification)

info_command = command_class.Command()

info_command.keys = ['верификация']
info_command.desciption = ''
info_command.payload = "verification_info"
info_command.process = info
