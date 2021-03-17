from .. import classes as command_class
from ..keyboards import getMainKeyboard
from ..classes import vk, MessageSettings, UserParams
import random


def info():

    message = """URL ссылка на календарь позволяет добавить ваше расписание в онлайн календари, например в Outlook. 
    Такое расписание не нужно скачивать, календарь автоматически скачает его по этой ссылке.
    Просто скопируйте эту ссылку и вставьте в ваш календарь.
    """
    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": message, "keyboard" : getMainKeyboard(UserParams.role),
                        "random_id": random.randint(1, 2147483647)})
    message = "https://dobrynin.engineer/download/shedule/?groupid={}".format(UserParams.groupId)
    vk.method("messages.send",
              {"peer_id": MessageSettings.getPeer_id(), "message": message,
               "keyboard": getMainKeyboard(UserParams.role),
               "random_id": random.randint(1, 2147483647)})

info_command = command_class.Command()

info_command.keys = ['url ссылка на календарь']
info_command.desciption = 'ссылка на календарь в Интернете для добавления в онлайн календари'
info_command.payload = "url_shed_ics"
info_command.process = info
