import command_class
import vk_api
import random
from main import vk
from message_class import MessageSettings
from user_class import UserParams
from keyboards import getMainKeyboard


def info():

    message = """Чат-бот расписание занятий уже почти год служит студентам и показывает персональное расписание занятий. 
    Он используется исключительно в информационных целях, оперирует данными с сайта kai.ru и не является официальным сервисом КНИТУ-КАИ.
    Будучи абитуриентом вы здесь можете узнать лишь ссылки на официальные источники, сайты и чаты КАИ.
    Для перехода в официальные источники воспользуйтесь клавиатурой ВКонтакте.
    """
    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": message, "keyboard" : getMainKeyboard(UserParams.role),
                        "random_id": random.randint(1, 2147483647)})

command = command_class.Command()

command.keys = ['что это', 'как', 'информация', 'инфа']
command.desciption = 'про бота для абитуриентов'
command.payload = "infoabiturient"
command.process = info
command.role = [4]
