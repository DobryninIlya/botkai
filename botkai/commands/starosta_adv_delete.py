from .. import classes as command_class
import random
from ..keyboards import GetButtonDeleteByDate
from ..classes import vk, MessageSettings


def info():

    vk.method("messages.send", {"peer_id": MessageSettings.id, "message": "Введите дату объявления, которое нужно удалить" , "keyboard": GetButtonDeleteByDate(), "random_id": random.randint(1, 2147483647)})
    

    return "ok"




command = command_class.Command()




command.keys = []
command.desciption = 'удаление объявлений старосты'
command.process = info
command.payload = "starosta_adv_delete"
command.admlevel = 2