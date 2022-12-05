from .. import classes as command_class
from ..keyboards import warnInfo
from ..classes import vk, cursor
import random
import datetime
import traceback


##################################                Добавить блокировку от 3 варнов
async def info(MessageSettings, user):
    id = MessageSettings.id
    try:

        cursor.execute('SELECT warn, expiration FROM Users WHERE ID_VK = ' + str(id))
        res = cursor.fetchone()
        warn = str(res[0])
        exp = str(res[1])
        result = "У вас " + warn + " предупреждений."
        if exp:
            result += "\n Истекают: " + exp
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message=result,
                               keyboard=warnInfo,
                               random_id=random.randint(1, 2147483647))
    except Exception:
        print('Ошибка:\n', traceback.format_exc())

    return "ok"


command = command_class.Command()

command.keys = ['предупреждения']
command.desciption = ''
command.process = info
command.payload = "warnlist"
command.role = [1, 2, 3, 4, 5]
