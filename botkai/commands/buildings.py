from .. import classes as command_class
from ..classes import vk, MessageSettings, UserParams
import random
import json
from ..keyboards import buildings_menu

def info():

    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": "Выберите здание", "keyboard" : buildings_menu,
                        "random_id": random.randint(1, 2147483647)})

info_command = command_class.Command()

info_command.keys = ['разное']
info_command.desciption = 'разное'
info_command.payload = "buildings_menu"
info_command.process = info

#comment
