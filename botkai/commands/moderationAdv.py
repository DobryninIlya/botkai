import random
import traceback

from .. import classes as command_class
from ..classes import vk, MessageSettings, UserParams, cursor
from ..keyboards import GetModerAdvButton

chetn = UserParams.getChetn()


def info():

    id = MessageSettings.getId()

    try:
        cursor.execute('SELECT * FROM "Adv" WHERE ischeked < 1 LIMIT 1')
        res = cursor.fetchone()
        
        vk.method("messages.send",
            {"peer_id": id, "message": "Начата модерация объявлений", "random_id": random.randint(1, 2147483647)})
        if res:
            ans = "Объявление §\n"
            ans += "\nid " + str(res[0]) + " from @id" + str(res[2])
            ans += "\n date: " + str(res[3])
            ans += "\n" + str(res[4])
            vk.method("messages.send",
                {"peer_id": id, "message": str(ans), "keyboard": GetModerAdvButton(res[0]), "random_id": random.randint(1, 2147483647)})
        else:
            vk.method("messages.send",
                {"peer_id": id, "message": "Все проверено", "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        vk.method("messages.send",
            {"peer_id": id, "message": "Произошла ошибка. Модерация", "random_id": random.randint(1, 2147483647)})

    return "ok"



command = command_class.Command()




command.keys = ['!moder adv', 'moder adv']
command.desciption = ''
command.process = info
command.payload = "moderadv"
command.admlevel = 4
command.role.append(2)
