from .. import classes as command_class
from ..keyboards import KeyboardProfile
from ..classes import vk, MessageSettings, UserParams, cursor, connection
import random
import traceback


def info():


    try:
        sql = "UPDATE users SET admLevel = 1 WHERE id_vk = {}".format(MessageSettings.getId())
        cursor.execute(sql)
        connection.commit()
        vk.method("messages.send", {"peer_id": MessageSettings.getId(), "message": "Ты успешно снят с должности старосты. Теперь стать старостой может кто-то другой. Если это ошибка, ты можешь занять пост старосты в профиле" ,"keyboard": KeyboardProfile(),  "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
    return "ok"

command = command_class.Command()

command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "starosta_leave"
