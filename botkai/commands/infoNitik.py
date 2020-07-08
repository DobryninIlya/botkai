import command_class
import vk_api
import random
from main import vk
from message_class import MessageSettings
from user_class import UserParams
from keyboards import getMainKeyboard


def info():

    message = """расписание - показать расписание ыыыы
    """
    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": message, "keyboard" : getMainKeyboard(UserParams.role),
                        "random_id": random.randint(1, 2147483647)})

info_command = command_class.Command()

info_command.keys = ['команды']
info_command.desciption = 'Покажу список команд'
info_command.payload = "infoNitik"
info_command.process = info
info_command.role = [5]