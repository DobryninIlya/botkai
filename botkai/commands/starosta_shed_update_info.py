import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import shed_update


async def info():
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="""Расписание хранится в буфере на сервере и автоматически обновляется с переодичностью в несколько дней. 
        Когда происходит запрос расписания, оно берется именно из буфера и может получиться так, что расписание окажется не актуальным.
        Эта функция служит для принудительного обновления расписания в Базе Данных сервера.""",
                           random_id=random.randint(1, 2147483647),
                           keyboard=shed_update)

    return "ok"





command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "starosta_shed_update_info"
command.admlevel = 2