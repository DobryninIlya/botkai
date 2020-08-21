from .. import classes as command_class
import random
from ..keyboards import GetButtonDeleteByDate
from ..classes import vk, MessageSettings, conn, cursorR
import traceback

def info():

    
    try:
        sql = "INSERT INTO Status VALUES (" + str(MessageSettings.id) + ", 46);"
        print(sql)
        cursorR.execute(sql)
        conn.commit()
        vk.method("messages.send", {"peer_id": MessageSettings.id, "message": "Отправь сообщение, которое нужно отослать, и прикрепи к нему медиавложения", "random_id": random.randint(1, 2147483647)})  
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        conn.rollback()
        vk.method("messages.send",
            {"peer_id": MessageSettings.id, "message": "Произошла ошибка. Повторите позже. (Рассылка сообщений)", "random_id": random.randint(1, 2147483647)})

    return "ok"





command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "make_admin_distr"
command.admlevel = 2