import random

from .. import classes as command_class
from ..classes import vk, cursor, connection


async def info(MessageSettings, user):
    cursor.execute("DELETE FROM users WHERE id_vk = {}".format(MessageSettings.getPeer_id()))
    connection.commit()
    message = """Ваш аккаунт был удален. Теперь вы можете пройти регистрацию заново! 
    Для этого достаточно отправить любое сообщение и я вам предложу пройти регистрацию еще раз.
    """
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=message,
                           random_id=random.randint(1, 2147483647))


command = command_class.Command()

command.keys = []
command.desciption = 'удаление аккаунта абитуриента'
command.payload = "undo_abiturient"
command.process = info
command.role = [4]
