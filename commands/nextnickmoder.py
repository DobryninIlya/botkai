import random
import traceback

from .. import classes as command_class
from ..classes import vk, connection, cursor
from ..keyboards import GetModerNickButton


##################################                Добавить блокировку от 3 варнов
async def info(MessageSettings, user):
    id = MessageSettings.getId()
    idAdv = MessageSettings.payload["id"]
    cursor.execute('UPDATE users SET ischeked = 1 WHERE ID_VK = ' + str(idAdv))
    connection.commit()
    try:
        cursor.execute('SELECT * FROM users WHERE ischeked < 1 LIMIT 1')
        res = cursor.fetchone()
        connection.commit()

        if res:
            ans = "Ник §\n"
            ans += "from @id" + str(res[0])
            ans += "\n" + str(res[1])
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message=str(ans),
                                   keyboard=GetModerNickButton(res[0]),
                                   random_id=random.randint(1, 2147483647))
        else:
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message="Все проверено",
                                   random_id=random.randint(1, 2147483647))
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Произошла ошибка. Модерация",
                               random_id=random.randint(1, 2147483647))
    return "ok"


command = command_class.Command()

command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "nextnick"
