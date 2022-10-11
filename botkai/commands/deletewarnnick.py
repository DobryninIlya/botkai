import datetime
import random
import traceback

from .. import classes as command_class
from ..classes import vk, MessageSettings, connection, cursor
from ..keyboards import warnList, GetModerNickButton


##################################                Добавить блокировку от 3 варнов
async def info():
    id = MessageSettings.id
    today = datetime.date.today()
    try:
        idAdv = MessageSettings.payload["id"]
        cursor.execute("UPDATE Users SET name = 'null' WHERE ID_VK = " + str(idAdv))
        cursor.execute("UPDATE Users SET ischeked = 1 WHERE ID_VK = " + str(idAdv))
        cursor.execute('SELECT warn FROM Users WHERE ID_VK = ' + str(idAdv))
        await vk.messages.send(peer_id=int(idAdv),
                               message="Ваш ник был удален модератором. Вероятно, он был некорректным. \n Также вам выдано 1 предупреждение.",
                               random_id=random.randint(1, 2147483647),
                               keyboard=warnList)
        warnCurr = int(cursor.fetchone()[0])
        warnCurr += 1
        cursor.execute('UPDATE Users SET warn = ' + str(warnCurr) + ' WHERE ID_VK = ' + str(idAdv))
        cursor.execute("UPDATE Users SET expiration = '" + str(datetime.date(today.year, today.month, today.day) + datetime.timedelta(days = 30)) + "' WHERE ID_VK = " + str(idAdv))
        connection.commit()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())

    try:
        cursor.execute('SELECT * FROM users WHERE ischeked < 1 LIMIT 1')
        res = cursor.fetchone()

        if res:
            ans = "Ник §\n"
            ans += "from @id" + str(res[0])
            ans += "\n" + str(res[1])
            await vk.messages.send(peer_id=id,
                                   message=str(ans),
                                   random_id=random.randint(1, 2147483647),
                                   keyboard=GetModerNickButton(res[0]))
        else:
            await vk.messages.send(peer_id=id,
                                   message="Все проверено",
                                   random_id=random.randint(1, 2147483647))
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        await vk.messages.send(peer_id=id,
                               message="Произошла ошибка. Модерация",
                               random_id=random.randint(1, 2147483647))
    return "ok"





command = command_class.Command()




command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "deletewarnnick"
