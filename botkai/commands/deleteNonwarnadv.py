import datetime
import random
import traceback

from .. import classes as command_class
from ..classes import vk, MessageSettings, connection, cursor
from ..keyboards import GetModerAdvButton


##################################                Добавить блокировку от 3 варнов
async def info():
    id = MessageSettings.id
    today = datetime.date.today()
    try:
        idAdv = MessageSettings.payload["id"]
        cursor.execute('SELECT * FROM "Adv" WHERE id = ' + str(idAdv))
        res = cursor.fetchone()
        cursor.execute('DELETE FROM "Adv" WHERE id = ' + str(idAdv))

        await vk.messages.send(peer_id=int(res[2]),
                               message="Одно из ваших объявлений было удалено модератором. Вероятно, оно было некорректным. \n",
                               random_id=random.randint(1, 2147483647))
        connection.commit()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())

    try:
        cursor.execute('SELECT * FROM "Adv" WHERE ischeked < 1 LIMIT 1')
        res = cursor.fetchone()
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Начата модерация объявлений",
                               random_id=random.randint(1, 2147483647))

        if res:
            ans = "Задание §\n"
            ans += "\nid " + str(res[0]) + " from @id" + str(res[2])
            ans += "\n date: " + str(res[3])
            ans += "\n" + str(res[4])
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message=str(res),
                                   random_id=random.randint(1, 2147483647),
                                   keyboard=GetModerAdvButton(res[0]),
                                   attachment=str(res[5]))
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
command.payload = "deleteadv"
