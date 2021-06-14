import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import make_starosta


def info():
    msg = """
    🙋 В твоей группе не назначен староста. В таком случае любой желающий может стать старостой, однако, это очень ответственная должность. 
    📖 Тебе будет доступен некоторый набор функций для поддержания порядка в группе.
    В группе может быть только один староста и в случае чего, есть возможность уйти с поста старосты без проблем.
    Не стоит баловаться этими возможностями, ведь вас может заблокировать администратор. 🙅‍♂️
    """
    vk.method("messages.send", {"peer_id": MessageSettings.getId(), "message": msg ,"keyboard": make_starosta, "random_id": random.randint(1, 2147483647)})
    return "ok"

command = command_class.Command()

command.keys = ['стать старостой']
command.desciption = ''
command.process = info
command.payload = "get_starosta"
