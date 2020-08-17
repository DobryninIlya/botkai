from .. import classes as command_class
from ..keyboards import GetDeleteTaskButton, keyboardTasks
from ..classes import vk, MessageSettings
import random
import sys

def info():
    id = MessageSettings.getId()

    vk.method("messages.send",
                        {"peer_id": id, "message": "Перезагрузка", "random_id": random.randint(1, 2147483647)})
    sys.exit(0)
    
      
    return "ok"



command = command_class.Command()




command.keys = ['reload']
command.desciption = 'рестарт'
command.process = info
command.payload = "reload"
command.admlevel = 90
