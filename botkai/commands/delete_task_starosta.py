from .. import classes as command_class
import random
from ..keyboards import KeyboardProfile
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import traceback

def info():
    groupId = UserParams.groupId
    payload = MessageSettings.payload
    id = payload["id"]
    print(id)
    try:
        sql = "DELETE FROM Task WHERE" + " id = " + str(id) + " AND userid = " + str(MessageSettings.getId()) + ";"
        print(sql)
        cursor.execute(sql)
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
    vk.method("messages.send", {"peer_id": MessageSettings.id, "message": "Удалено" , "keyboard": KeyboardProfile(), "random_id": random.randint(1, 2147483647)})
    

    return "ok"




command = command_class.Command()




command.keys = []
command.desciption = 'удаление по id'
command.process = info
command.payload = "deletetask_starosta"