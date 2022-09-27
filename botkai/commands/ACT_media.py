import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import activities_hub_event




def info():

    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": "Бот расписание занятий КНИТУ-КАИ",
                     "keyboard": activities_hub_event,
                        "random_id": random.randint(1, 2147483647)})


info_command = command_class.Command()

info_command.keys = ['Творческое медиа-пространство КАИ']
info_command.desciption = ''
info_command.payload = "ACT_media"
info_command.process = info
