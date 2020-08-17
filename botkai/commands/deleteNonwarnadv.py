from .. import classes as command_class
from ..keyboards import GetModerAdvButton
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random
import traceback
import datetime
##################################                Добавить блокировку от 3 варнов 
def info():
    id = MessageSettings.id
    today = datetime.date.today()
    try:
        idAdv = MessageSettings.payload["id"]
        cursor.execute('SELECT * FROM "Adv" WHERE id = ' + str(idAdv))
        res = cursor.fetchone()
        cursor.execute('DELETE FROM "Adv" WHERE id = ' + str(idAdv))
    

        vk.method("messages.send",
            {"peer_id": int(res[2]), "message": "Одно из ваших объявлений было удалено модератором. Вероятно, оно было некорректным. \n", "random_id": random.randint(1, 2147483647)})
        connection.commit()
        print("succs")
    except Exception:
        print('Ошибка:\n', traceback.format_exc())

    try:
        #sql = "INSERT INTO Status VALUES (" + str(id) + ", 100);"
        #cursorR.execute(sql)
        #conn.commit()
        #conn.close()
        cursor.execute('SELECT * FROM "Adv" WHERE ischeked < 1 LIMIT 1')
        res = cursor.fetchone()
        
        vk.method("messages.send",
            {"peer_id": id, "message": "Начата модерация объявлений", "random_id": random.randint(1, 2147483647)})
        if res:
            ans = "Задание §\n"
            ans += "\nid " + str(res[0]) + " from @id" + str(res[2])
            ans += "\n date: " + str(res[3])
            ans += "\n" + str(res[4])
            vk.method("messages.send",
                {"peer_id": id, "message": str(res), "keyboard": GetModerAdvButton(res[0]),'attachment': str(res[5]), "random_id": random.randint(1, 2147483647)})
        else:
            vk.method("messages.send",
                {"peer_id": id, "message": "Все проверено", "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        #conn.rollback()
        vk.method("messages.send",
            {"peer_id": id, "message": "Произошла ошибка. Модерация", "random_id": random.randint(1, 2147483647)})
    return "ok"





command = command_class.Command()




command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "deleteadv"
