from .. import classes as command_class
import random
from ..keyboards import shed_update
from ..classes import vk, MessageSettings, conn, cursorR
import traceback

def info():

    vk.method("messages.send",
        {"peer_id": MessageSettings.id, "message": """Расписание хранится в буфере на сервере и автоматически обновляется с переодичностью в несколько дней. 
        Когда происходит запрос расписания, оно берется именно из буфера и может получиться так, что расписание окажется не актуальным.
        Эта функция служит для принудительного обновления расписания в Базе Данных сервера.""","keyboard": shed_update, "random_id": random.randint(1, 2147483647)})

    return "ok"





command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "starosta_shed_update_info"
command.admlevel = 2