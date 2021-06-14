import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import submenu


def info():

    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": "Здесь скоро будет информация по кружкам, советам и другим творческим объединениям. \n Глава такого объединения? Напиши мне ( @ilya_dobrynin ), чтобы оказаться здесь и о тебе узнали люди", 
                    "keyboard" : submenu,
                        "random_id": random.randint(1, 2147483647)})

info_command = command_class.Command()

info_command.keys = ['активности']
info_command.desciption = 'доп меню'
info_command.payload = "activities"
info_command.process = info
