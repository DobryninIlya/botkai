from .. import classes as command_class
import random
from ..keyboards import week_shed_kbrd
from ..classes import vk, MessageSettings, UserParams, connection, cursor

def info():
    
    id = MessageSettings.getId()
    
    vk.method("messages.send",
                        {"peer_id": id, "message": "меню","keyboard" : week_shed_kbrd, "random_id": random.randint(1, 2147483647)})

    
      
    return "ok"



command = command_class.Command()




command.keys = ["рассылки", "управление рассылками"]
command.desciption = ''
command.process = info
command.payload = "distr"

