import random
import traceback

from .. import classes as command_class
from ..classes import vk, MessageSettings, conn, cursorR


def info():

    
    try:
        sql = "INSERT INTO Status VALUES (" + str(MessageSettings.id) + ", 48);"
        # print(sql)
        cursorR.execute(sql)
        conn.commit()
        vk.method("messages.send", {"peer_id": MessageSettings.id, "message": "Отправь мне ссылку того, кого нужно кикнуть из группы", "random_id": random.randint(1, 2147483647)})  
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        conn.rollback()
        vk.method("messages.send",
            {"peer_id": MessageSettings.id, "message": "Произошла ошибка. Повторите позже", "random_id": random.randint(1, 2147483647)})

    return "ok"





command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "make_kick"
command.admlevel = 2