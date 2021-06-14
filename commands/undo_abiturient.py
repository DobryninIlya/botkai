import random

from .. import classes as command_class
from ..classes import vk, MessageSettings, cursor, connection


def info():
    cursor.execute("DELETE FROM users WHERE id_vk = {}".format(MessageSettings.getPeer_id()))
    connection.commit()
    message = """Ваш аккаунт был удален. Теперь вы можете пройти регистрацию заново! 
    Для этого достаточно отправить любое сообщение и я вам предложу пройти регистрацию еще раз.
    """
    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": message,
                        "random_id": random.randint(1, 2147483647)})

command = command_class.Command()

command.keys = []
command.desciption = 'удаление аккаунта абитуриента'
command.payload = "undo_abiturient"
command.process = info
command.role = [4]
