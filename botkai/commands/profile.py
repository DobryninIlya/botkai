from .. import classes as command_class
import random
from ..keyboards import KeyboardProfile
from ..classes import vk as vk
from ..classes import MessageSettings
from ..classes import UserParams


def info():
    id = MessageSettings.getPeer_id()
    message = "Профиль"
    vk.method("messages.send",
                    {"peer_id": id, "keyboard" : KeyboardProfile(),
                        "random_id": random.randint(1, 2147483647)})

command = command_class.Command()

command.keys = ['профиль', 'настройки']
command.desciption = 'Покажу твой профиль'
command.process = info
command.payload = "profile"