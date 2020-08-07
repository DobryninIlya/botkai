from .. import classes as command_class
import random
from ..keyboards import GetStarostaKeyboard
from ..classes import vk, MessageSettings, conn, cursorR
import traceback

def info():

    vk.method("messages.send",
        {"peer_id": MessageSettings.id, "message": "Меню старосты","keyboard": GetStarostaKeyboard(), "random_id": random.randint(1, 2147483647)})

    return "ok"





command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "starosta_menu"
command.admlevel = 2