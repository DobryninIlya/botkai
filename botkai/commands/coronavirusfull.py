from .. import classes as command_class
import random
from ..keyboards import coronavirusfull as keyboard
from ..classes import vk, MessageSettings


def info():
    id = MessageSettings.getId()
    vk.method("messages.send",
                        {"peer_id": id, "message": "Выберите пункт меню", "keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
    
      
    return "ok"



command = command_class.Command()




command.keys = ['коронавирус', 'карантин']
command.desciption = ''
command.process = info
command.payload = "coronavirusfull"

