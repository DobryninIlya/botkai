import random
import sys

from .. import classes as command_class
from ..classes import vk, MessageSettings


def info():
    id = MessageSettings.getId()

    vk.method("messages.send",
                        {"peer_id": id, "message": "Перезагрузка", "random_id": random.randint(1, 2147483647)})
    sys.exit(1)
      
    return "ok"



command = command_class.Command()




command.keys = ['reload']
command.desciption = 'рестарт'
command.process = info
command.payload = "reload"
command.admlevel = 90
