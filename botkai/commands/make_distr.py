import random
import traceback

from .. import classes as command_class
from ..classes import vk, conn, cursorR


async def info(MessageSettings, user):
    try:
        sql = "INSERT INTO Status VALUES (" + str(MessageSettings.id) + ", 47);"
        # print(sql)
        cursorR.execute(sql)
        conn.commit()
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Отправь сообщение, которое нужно отослать, и прикрепи к нему медиавложения",
                               random_id=random.randint(1, 2147483647))
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        conn.rollback()
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Произошла ошибка. Повторите позже. (Рассылка сообщений)",
                               random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "make_distr"
command.admlevel = 2
