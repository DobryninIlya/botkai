from .. import classes as command_class
from ..keyboards import keyboardPrepodShareMessage
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random
import datetime

uptime = datetime.datetime.now()


def info():
    vk.method("messages.send",
              {"peer_id": MessageSettings.getId(), "message": "Вы можете отослать своим студентам сообщение. "
                                                              "Можно прикрепить медиавложения.",
               "keyboard": keyboardPrepodShareMessage, "random_id": random.randint(1, 2147483647)})

    return "ok"


command = command_class.Command()

command.keys = ['Отправить сообщение студентам справка']
command.description = 'связь со студентами справка'
command.process = info
command.payload = "prepod_share_message_info"
command.role = [2]
