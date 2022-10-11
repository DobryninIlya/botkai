import datetime
import random
import traceback

from .. import classes as command_class
from ..classes import vk, MessageSettings, connection, cursor
from ..keyboards import warnList, GetModerTaskButton


async def info():
    id = MessageSettings.id
    today = datetime.date.today()
    try:
        idAdv = MessageSettings.payload["id"]
        cursor.execute('SELECT * FROM Task WHERE id = ' + str(idAdv))
        res = cursor.fetchone()
        cursor.execute('DELETE FROM Task WHERE id = ' + str(idAdv))
    
        cursor.execute('SELECT warn FROM Users WHERE ID_VK = ' + str(res[2]))
        await vk.messages.send(peer_id=int(res[2]),
                               message="Одно из ваших заданий было удалено модератором. Вероятно, оно было некорректным. \n Также вам выдано 1 предупреждение.",
                               keyboard=warnList,
                               random_id=random.randint(1, 2147483647))
        warnCurr = int(cursor.fetchone()[0])
        warnCurr += 1
        cursor.execute('UPDATE Users SET warn = ' + str(warnCurr) + ' WHERE ID_VK = ' + str(res[2]))
        cursor.execute("UPDATE Users SET expiration = '" + str(datetime.date(today.year, today.month, today.day) + datetime.timedelta(days = 30)) + "' WHERE ID_VK = " + str(res[2]))
        connection.commit()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())

    try:
        cursor.execute('SELECT * FROM Task WHERE "IsCheked" < 1 LIMIT 1')
        res = cursor.fetchone()
        
        
        if res:
            ans = "Задание §\n"
            ans += "\nid " + str(res[0]) + " from @id" + str(res[2])
            ans += "\n date: " + str(res[3])
            ans += "\n" + str(res[4])
            await vk.messages.send(peer_id=id,
                                   message=str(ans),
                                   keyboard=GetModerTaskButton(res[0]),
                                   random_id=random.randint(1, 2147483647),
                                   attachment=str(res[5]))
        else:
            await vk.messages.send(peer_id=id,
                                   message="Все проверено",
                                   random_id=random.randint(1, 2147483647))
            vk.method("messages.send",
                {"peer_id": id, "message": "Все проверено", "random_id": random.randint(1, 2147483647)})
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
command.payload = "deletewarntask"
