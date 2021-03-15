from .. import classes as command_class
import random
from ..keyboards import GetAdminPanel
from ..classes import vk, MessageSettings, UserParams


def info():
    id = MessageSettings.getId()

    vk.method("messages.send",
                        {"peer_id": id, "message": "Apanel","keyboard": GetAdminPanel(UserParams.getAdminLevel()), "random_id": random.randint(1, 2147483647)})

    return "ok"



command = command_class.Command()




command.keys = ['apanel']
command.desciption = 'админ панель'
command.process = info
command.payload = "apanel"
command.admlevel = 4
command.role.append(2)
