from .. import classes as command_class
from ..keyboards import getMainKeyboard
from ..classes import vk
import random


async def info(MessageSettings, user):

    message = """Чат-бот расписание занятий уже год служит студентам и показывает персональное расписание занятий. 
    Он используется исключительно в информационных целях, оперирует данными с сайта kai.ru и не является официальным сервисом КНИТУ-КАИ.
    Будучи абитуриентом вы здесь можете узнать лишь ссылки на официальные источники, сайты и чаты КАИ.
    Для перехода в официальные источники воспользуйтесь клавиатурой ВКонтакте.
    """
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=message,
                           keyboard=getMainKeyboard(user.role),
                           random_id=random.randint(1, 2147483647))


command = command_class.Command()

command.keys = ['что это', 'как', 'информация', 'инфа']
command.desciption = 'про бота для абитуриентов'
command.payload = "infoabiturient"
command.process = info
command.role = [4]
