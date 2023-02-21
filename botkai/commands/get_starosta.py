import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import make_starosta


async def info(MessageSettings, user):
    msg = """
    🙋 В твоей группе не назначен староста. В таком случае любой желающий может стать старостой, однако, это очень ответственная должность. 
    📖 Тебе будет доступен некоторый набор функций для поддержания порядка в группе.
    В группе может быть только один староста и в случае чего, есть возможность уйти с поста старосты без проблем.
    Не стоит баловаться этими возможностями, ведь вас может заблокировать администратор. 🙅‍♂️
    """
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=msg,
                           random_id=random.randint(1, 2147483647),
                           keyboard=make_starosta)
    return "ok"


command = command_class.Command()

command.keys = ['стать старостой']
command.desciption = ''
command.process = info
command.payload = "get_starosta"
