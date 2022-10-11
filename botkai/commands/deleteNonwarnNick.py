import datetime
import random
import traceback

from .. import classes as command_class
from ..classes import vk, MessageSettings, connection, cursor
from ..keyboards import GetModerNickButton


##################################                Добавить блокировку от 3 варнов 
async def info():
    id = MessageSettings.id
    today = datetime.date.today()
    try:
        idAdv = MessageSettings.payload["id"]
        # cursor.execute('SELECT * FROM Users WHERE ID_VK = ' + str(idAdv))
        # res = cursor.fetchone()
        cursor.execute("UPDATE Users SET name = 'null' WHERE ID_VK = " + str(idAdv))
        cursor.execute("UPDATE Users SET ischeked = 1 WHERE ID_VK = " + str(idAdv))
        await vk.messages.send(peer_id=int(idAdv),
                               message="Ваш ник был удален модератором. Вероятно, он был некорректным. \n",
                               random_id=random.randint(1, 2147483647))
        connection.commit()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())

    try:
        cursor.execute('SELECT * FROM Users WHERE ischeked < 1 LIMIT 1')
        res = cursor.fetchone()

        if res:
            ans = "Ник §\n"
            ans += "from @id" + str(res[0])
            ans += "\n" + str(res[1])
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message=str(ans),
                                   random_id=random.randint(1, 2147483647),
                                   keyboard=GetModerNickButton(res[0]),
                                   attachment=str(res[5]))
        else:
            vk.method("messages.send",
                      {"peer_id": id, "message": "Все проверено", "random_id": random.randint(1, 2147483647)})
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
command.payload = "deletenick"
