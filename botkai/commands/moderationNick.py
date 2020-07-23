from .. import classes as command_class
from ..keyboards import GetModerAdvButton
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random



chetn = UserParams.getChetn()




def info():
    id = MessageSettings.getId()
    try:
        cursor.execute('SELECT * FROM Users WHERE ischeked < 1 LIMIT 1')
        res = cursor.fetchone()
        
        vk.method("messages.send",
            {"peer_id": id, "message": "Начата модерация ников", "random_id": random.randint(1, 2147483647)})
        if res:
            ans = "Ник §\n"
            ans += "from @id" + str(res[0])
            ans += "\n" + str(res[1])
            vk.method("messages.send",
                {"peer_id": id, "message": str(ans), "keyboard": GetModerNickButton(res[0]), "random_id": random.randint(1, 2147483647)})
        else:
            vk.method("messages.send",
                {"peer_id": id, "message": "Все проверено", "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        vk.method("messages.send",
            {"peer_id": id, "message": "Произошла ошибка. Модерация", "random_id": random.randint(1, 2147483647)})

    return "ok"



command = command_class.Command()




command.keys = ['!moder nick', 'moder nick']
command.desciption = ''
command.process = info
command.payload = "modernick"
command.admlevel = 4
