from .. import classes as command_class
from ..keyboards import warnInfo
from ..classes import vk, MessageSettings, cursor
import random
import datetime

##################################                Добавить блокировку от 3 варнов 
def info():
    id = MessageSettings.id
    today = datetime.date.today()
    try:

        cursor.execute('SELECT warn, expiration FROM Users WHERE ID_VK = ' + str(id))
        res = cursor.fetchone()
        warn = str(res[0])
        exp = str(res[1])
        result = "У вас " + warn + " предупреждений."
        if exp:
            result += "\n Истекают: " + exp
        vk.method("messages.send",
                {"peer_id": id, "message": result,"keyboard" : warnInfo, "random_id": random.randint(1, 2147483647)})
    except Exception:
        print('Ошибка:\n', traceback.format_exc())

    return "ok"





command = command_class.Command()




command.keys = ['предупреждения']
command.desciption = ''
command.process = info
command.payload = "warnlist"
