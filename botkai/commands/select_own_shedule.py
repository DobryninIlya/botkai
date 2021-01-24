from .. import classes as command_class
import random
from ..keyboards import KeyboardProfile
from ..classes import vk, MessageSettings, UserParams, cursor, connection


def info():
    id = MessageSettings.getId()

    if UserParams.own_shed:
        cursor.execute("UPDATE Users SET has_own_shed = False WHERE id_vk = {}".format(id))
        connection.commit()
        vk.method("messages.send",
                  {"peer_id": id,
                   "message": "Будет отображаться публичное расписание вашей группы",
                   "keyboard": KeyboardProfile(), "random_id": random.randint(1, 2147483647)})

    else:
        cursor.execute("UPDATE Users SET has_own_shed = True WHERE id_vk = {}".format(id))
        connection.commit()
        vk.method("messages.send",
                  {"peer_id": id,
                   "message": "Будет отображаться ваше сохраненное расписание из эксель таблицы",
                   "keyboard": KeyboardProfile(), "random_id": random.randint(1, 2147483647)})

    return "ok"



command = command_class.Command()




command.keys = ['способ получения расписания']
command.desciption = 'способ получения расписания'
command.process = info
command.payload = "select_own_shedule"