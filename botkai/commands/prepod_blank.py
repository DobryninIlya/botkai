import random

from ..keyboards import exit
from .. import classes as command_class
from ..classes import vk, cursorR, conn


async def info(MessageSettings, user):
    msg = "Введите номер группы"
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=msg,
                           random_id=random.randint(1, 2147483647))
    cursorR.execute("INSERT INTO Status VALUES ({},{})".format(MessageSettings.getId(), 307))
    conn.commit()
    return "ok"





command = command_class.Command()




command.keys = ['бланк посещения', "журнал посещения"]
command.desciption = 'отображение полного списка группы'
command.process = info
command.payload = "prepod_blank"
command.role = [2]