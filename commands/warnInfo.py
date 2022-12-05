from .. import classes as command_class
from ..classes import vk
import random


##################################                Добавить блокировку от 3 варнов
async def info(MessageSettings, user):
    res = """
    Предупреждения выдаются за различные нарушения на личное усмотрение администратора.
    Предупреждения обнуляются через 30 дней после его получения.
    Возможно досрочное снятие предупреждений за внутреннюю валюту. (пока недоступно)
    После получения 3-его предупреждения ваш аккаунт может быть заблокирован.

    """
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=res,
                           random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = ['инфа предупреждения']
command.desciption = ''
command.process = info
command.payload = "warnInfo"
command.role = [1, 2, 3, 4, 5]
