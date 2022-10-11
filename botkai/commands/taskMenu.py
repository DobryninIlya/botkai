from .. import classes as command_class
from ..keyboards import keyboardTasks
from ..classes import vk, MessageSettings
import random
import traceback


async def info():
    try:
        id = MessageSettings.getPeer_id()
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message='Выберите пункт меню:',
                               keyboard=keyboardTasks,
                               random_id=random.randint(1, 2147483647))
    except:
        print('Ошибка:\n', traceback.format_exc())


command = command_class.Command()

command.keys = ["задание", "задания"]
command.desciption = 'меню заданий'
command.process = info
command.payload = "task menu"
command.role = [1, 2, 3, 6]
