import random
import traceback

from .. import classes as command_class
from ..classes import vk, MessageSettings, UserParams, cursor

event_data = """{
    "type": "show_snackbar",
    "text": "Задание удалено"
  }"""

def info():
    groupId = UserParams.groupId
    payload = MessageSettings.payload
    id = payload["id"]
    # print(id)
    try:
        sql = "DELETE FROM Task WHERE" + " id = " + str(id)
        # print(sql)
        cursor.execute(sql)
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
    #vk.method("messages.send", {"peer_id": MessageSettings.id, "message": "Удалено" , "keyboard": KeyboardProfile(), "random_id": random.randint(1, 2147483647)})
    vk.method("messages.sendMessageEventAnswer",
                    {"event_id": MessageSettings.event_id,
                    "user_id": MessageSettings.id,
                    "peer_id": MessageSettings.peer_id,
                    "event_data": event_data
                    })

    
    vk.method("messages.edit", {
        "peer_id": MessageSettings.getId(),
        "message": "Задание было удалено..." , 
        "conversation_message_id" : MessageSettings.conversation_message_id,
        "random_id": random.randint(1, 2147483647)})

    return "ok"




command = command_class.Command()




command.keys = []
command.desciption = 'удаление по id'
command.process = info
command.payload = "deletetask_starosta"
command.admlevel = 2