import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import buildings_menu


def info():

    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": "Помогу в написании программной реализации проекта"
                                                                         "Напишу программу с GUI интерфейсом или чат-бота на "
                                                                         "интересную тему. Пишите с вопросами в личные сообщения."
                                                                         "Все конфиденциально.",
                        "random_id": random.randint(1, 2147483647)})

info_command = command_class.Command()

info_command.keys = []
info_command.desciption = 'разработка дипломов'
info_command.payload = "commerce"
info_command.process = info

#comment
