import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import activities_hub


async def info():
    msg = """Казанская Лига Дебатов:
Информацию о ближайших турнирах, о формате игры и в целом о дебатах читайте в группе казанских дебатов —
@kazan_debate"""
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=msg,
                           random_id=random.randint(1, 2147483647))


info_command = command_class.Command()

info_command.keys = ['информация клуб дебатов']
info_command.desciption = ''
info_command.payload = "act_media_debati_info"
info_command.process = info
