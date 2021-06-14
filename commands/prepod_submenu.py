import datetime
import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import keyboardPrepodSubmenu

uptime = datetime.datetime.now()

def info():

    vk.method("messages.send",
                        {"peer_id": MessageSettings.getId(), "message": "Меню", "keyboard": keyboardPrepodSubmenu, "random_id": random.randint(1, 2147483647)})
    
      
    return "ok"



command = command_class.Command()




command.keys = ['Связь со студентами']
command.description = 'связь со студентами'
command.process = info
command.payload = "prepod_submenu"
command.role = [2]
