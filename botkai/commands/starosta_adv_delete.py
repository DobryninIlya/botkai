from .. import classes as command_class
import random
from ..keyboards import GetButtonDeleteByDate
from ..classes import vk, MessageSettings, conn, cursorR


def info():

    
    try:
        sql = "INSERT INTO Status VALUES (" + str(id) + ", 57);"
        cursorR.execute(sql)
        conn.commit()
        vk.method("messages.send", {"peer_id": MessageSettings.id, "message": "Введите дату объявления, которое нужно удалить" , "keyboard": GetButtonDeleteByDate(), "random_id": random.randint(1, 2147483647)})  
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        conn.rollback()
        vk.method("messages.send",
            {"peer_id": id, "message": "Произошла ошибка. Повторите позже", "random_id": random.randint(1, 2147483647)})

    return "ok"





command = command_class.Command()




command.keys = []
command.desciption = 'удаление объявлений старосты'
command.process = info
command.payload = "starosta_adv_delete"
command.admlevel = 2