from .. import classes as command_class
import random
from ..keyboards import KeyboardProfile
from ..classes import vk, cursor, connection


async def info(MessageSettings, user):
    id = MessageSettings.getId()

    if user.own_shed:
        cursor.execute("UPDATE Users SET has_own_shed = False WHERE id_vk = {}".format(id))
        connection.commit()
        user.own_shed = 0
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Будет отображаться публичное расписание вашей группы",
                               keyboard=KeyboardProfile(MessageSettings, user),
                               random_id=random.randint(1, 2147483647))


    else:
        cursor.execute("UPDATE Users SET has_own_shed = True WHERE id_vk = {}".format(id))
        connection.commit()
        user.own_shed = 1
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Будет отображаться ваше сохраненное расписание из эксель таблицы",
                               keyboard=KeyboardProfile(MessageSettings, user),
                               random_id=random.randint(1, 2147483647))


    return "ok"


command = command_class.Command()


command.keys = ['способ получения расписания']
command.description = 'способ получения расписания'
command.process = info
command.payload = "select_own_shedule"
