from .. import classes as command_class
from ..keyboards import GetStarostaKeyboard, getMainKeyboard
from ..classes import vk, MessageSettings, UserParams, cursor, connection
import random
import traceback


def info():


    sql = "SELECT COUNT(*) FROM users WHERE users.groupp = {} AND admLevel = 2".format(UserParams.groupId)
    cursor.execute(sql)
    starosta_count = cursor.fetchone()[0]
    if starosta_count < 1:
        sql = "UPDATE users SET admLevel = 2 WHERE id_vk = {}".format(MessageSettings.getId())
        cursor.execute(sql)
        connection.commit()
        vk.method("messages.send", {"peer_id": MessageSettings.getId(), "message": "✅ Поздравляю! Теперь ты староста!" ,"keyboard": GetStarostaKeyboard(),  "random_id": random.randint(1, 2147483647)})
    else:
        vk.method("messages.send", {"peer_id": MessageSettings.getId(), "message": """❌ Ошибка. В группе уже назначен староста. 
        Если ты настоящий староста и претендуешь на это место, напиши администратору по кнопке Обратной связи в главном меню. Будь готов предоставить доказательства""",
        "keyboard": getMainKeyboard(),  "random_id": random.randint(1, 2147483647)})
    return "ok"

command = command_class.Command()

command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "make_starosta"
