import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import help_starosta_upload


async def info():
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=("Для загрузки расписания из Excel таблицы ознакомьтесь с инструкцией\n"
                                    "        Чтобы расписание обновилось у всей группы, используйте команду 'Загрузить расписание староста', когда будете прикреплять заполненный Execl файл\n"),
                           keyboard=help_starosta_upload,
                           random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = ['Расписание старосты', 'Сделать расписание для группы']
command.desciption = ''
command.process = info
command.payload = "starostaexcel"
#
