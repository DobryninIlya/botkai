import random

from .. import classes as command_class


from ..classes import vk as vk
from ..keyboards import getMainKeyboard


async def info(MessageSettings, user):
    message = """профиль - меню профиля
    на завтра/сегодня/послезавтра - расписание на завтра
    полностью - список полного расписания
    донат - пожертвования боту/пополнение баланса
    преподаватели - список преподавателей
    четность - покажу, четная или нечетная неделя
    поток - включить/выключить отображение потоковых лекций
    """
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=message,
                           keyboard=getMainKeyboard(user.role),
                           random_id=random.randint(1, 2147483647))


info_command = command_class.Command()

info_command.keys = ['список команд', 'команды', 'помоги']
info_command.desciption = 'Покажу список команд'
info_command.payload = "commands"
info_command.process = info
info_command.role = [1, 2, 3, 6]
