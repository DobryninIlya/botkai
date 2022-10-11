import random
import traceback

from .. import classes as command_class
from ..classes import vk, MessageSettings, UserParams, cursor
from ..keyboards import KeyboardProfile


async def info():
    groupId = UserParams.groupId
    payload = MessageSettings.payload
    id = payload["id"]
    # print(id)
    try:
        sql = "DELETE FROM Task WHERE" + " id = " + str(id) + " AND userid = " + str(MessageSettings.getId()) + ";"
        # print(sql)
        cursor.execute(sql)
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Удалено",
                           random_id=random.randint(1, 2147483647),
                           keyboard=KeyboardProfile())

    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = 'удаление по id'
command.process = info
command.payload = "deletetask"
