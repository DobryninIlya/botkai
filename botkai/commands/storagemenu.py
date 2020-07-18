from .. import classes as command_class
from ..keyboards import keyboard.storageMain
from ..classes import vk, MessageSettings
import random


def info():
    
    id = MessageSettings.getId()
    flag = False
    if flag:
        vk.method("messages.send",
            {"peer_id": MessageSettings.getPeer_id(), "message": "☣️ Отдел закрыт :(", "keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
        return "ok"
    vk.method("messages.send",
                        {"peer_id": id, "message": "Хранилище. Выбери пункт меню","keyboard" : storageMain, "random_id": random.randint(1, 2147483647)})

    
      
    return "ok"



command = command_class.Command()




command.keys = ["что такое хранилище", 'хранилище']
command.desciption = ''
command.process = info
command.payload = "storagemain"

