import classes as command_class
import vk_api
import random
from main import vk
from message_class import MessageSettings
from user_class import UserParams
from keyboards import getMainKeyboard


def info():

    message = """профиль - меню профиля
    на завтра/сегодня/послезавтра - расписание на завтра
    полностью - список полного расписания
    донат - пожертвования боту/пополнение баланса
    преподы - список преподавателей
    четность - покажу, четная или нечетная неделя
    """
    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": message, "keyboard" : getMainKeyboard(UserParams.role),
                        "random_id": random.randint(1, 2147483647)})

info_command = command_class.Command()

info_command.keys = ['список команд', 'команды', 'помоги']
info_command.desciption = 'Покажу список команд'
info_command.payload = "commands"
info_command.process = info
