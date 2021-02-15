from .. import classes as command_class
from ..keyboards import help_starosta_upload
from ..classes import vk, MessageSettings, UserParams, cursor, connection
import random
import traceback


def info():

    vk.method("messages.send", {"peer_id": MessageSettings.getId(), "message":
        """Для загрузки расписания из Excel таблицы ознакомьтесь с инструкцией
        Чтобы расписание обновилось у всей группы, используйте команду 'Загрузить расписание староста', когда будете прикреплять заполненный Execl файл
        """ ,"keyboard": help_starosta_upload,  "random_id": random.randint(1, 2147483647)})

    return "ok"

command = command_class.Command()

command.keys = ['Расписание старосты','Сделать расписание для группы']
command.desciption = ''
command.process = info
command.payload = "starostaexcel"
#