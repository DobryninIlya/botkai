import random

from .. import classes as command_class
from ..classes import vk, MessageSettings, UserParams, cursor, connection
from ..keyboards import GetStarostaKeyboard, getMainKeyboard


async def info():
    sql = "SELECT COUNT(*) FROM users WHERE users.groupp = {} AND admLevel = 2".format(UserParams.groupId)
    cursor.execute(sql)
    starosta_count = cursor.fetchone()[0]
    if starosta_count < 1:
        sql = "UPDATE users SET admLevel = 2 WHERE id_vk = {}".format(MessageSettings.getId())
        cursor.execute(sql)
        connection.commit()
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="✅ Поздравляю! Теперь ты староста!",
                               keyboard=GetStarostaKeyboard(1),
                               random_id=random.randint(1, 2147483647))
    else:
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="""❌ Ошибка. В группе уже назначен староста. 
        Если ты настоящий староста и претендуешь на это место, напиши администратору по кнопке Обратной связи в 
        главном меню. Будь готов предоставить доказательства""",
                               keyboard=getMainKeyboard(UserParams.role),
                               random_id=random.randint(1, 2147483647))
    return "ok"


command = command_class.Command()

command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "make_starosta"
