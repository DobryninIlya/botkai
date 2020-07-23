from .. import classes as command_class
from ..keyboards import testButtons
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random



chetn = UserParams.getChetn()




def info():

    id = MessageSettings.getId()

    vk.method("messages.send",
        {"peer_id": id, "message": str(ans), "keyboard": testButtons, "random_id": random.randint(1, 2147483647)})


    return "ok"



command = command_class.Command()




command.keys = ['test buttons']
command.desciption = ''
command.process = info
command.payload = ""

