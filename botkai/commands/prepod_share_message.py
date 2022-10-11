import datetime
import random

from .. import classes as command_class
from ..classes import vk, MessageSettings, conn, cursorR
from ..keyboards import exit

uptime = datetime.datetime.now()


async def info():
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Введите номер группы, студентам которой "
                                   "будет разослано сообщение",
                           keyboard=exit,
                           random_id=random.randint(1, 2147483647))
    cursorR.execute("INSERT INTO Status VALUES ({},{})".format(MessageSettings.getId(), 301))
    conn.commit()

    return "ok"


command = command_class.Command()

command.keys = ['Отправить сообщение студентам']
command.description = 'связь со студентами'
command.process = info
command.payload = "prepod_share_message_next"
command.role = [2]
