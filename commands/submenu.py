import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import submenu


def info():

    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": "Меню", "keyboard" : submenu,
                        "random_id": random.randint(1, 2147483647)})

info_command = command_class.Command()

info_command.keys = ['разное', 'дополнительное меню']
info_command.desciption = 'доп меню'
info_command.payload = "submenu"
info_command.process = info
