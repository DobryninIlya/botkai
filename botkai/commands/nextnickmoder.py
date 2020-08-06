from .. import classes as command_class
from ..keyboards import GetModerNickButton
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random
import traceback
##################################                Добавить блокировку от 3 варнов 
def info():
    id = MessageSettings.getId()
    idAdv = MessageSettings.payload["id"]
    cursor.execute('UPDATE users SET ischeked = 1 WHERE ID_VK = ' + str(idAdv))
    connection.commit()
    try:
        # sql = "INSERT INTO Status VALUES (" + str(id) + ", 100);"
        # cursorR.execute(sql)
        # conn.commit()
        # conn.close()
        cursor.execute('SELECT * FROM users WHERE ischeked < 1 LIMIT 1')
        res = cursor.fetchone()
        connection.commit()

        if res:
            ans = "Ник §\n"
            ans += "from @id" + str(res[0])
            ans += "\n" + str(res[1])
            vk.method("messages.send",
                      {"peer_id": id, "message": str(ans), "keyboard": GetModerNickButton(res[0]),
                       "random_id": random.randint(1, 2147483647)})
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
command.payload = "nextnick"
