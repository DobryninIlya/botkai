from .. import classes as command_class
from ..keyboards import keyboardPrepodShareMessage
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random
import datetime

uptime = datetime.datetime.now()


def info():
    vk.method("messages.send",
              {"peer_id": MessageSettings.getId(), "message": "Введите номер группы, студентам которой "
                                                              "будет разослано сообщение",
               "keyboard": keyboardPrepodShareMessage, "random_id": random.randint(1, 2147483647)})
    cursor.execute("INSERT INTO Status VALUES ()".format(MessageSettings.getId(), 301))
    connection.commit()

    return "ok"


command = command_class.Command()

command.keys = ['Отправить сообщение студентам']
command.description = 'связь со студентами'
command.process = info
command.payload = "prepod_share_message_info"
command.role = [2]
