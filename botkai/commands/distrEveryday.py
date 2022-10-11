import json
import random

from .. import classes as command_class
from ..classes import vk, MessageSettings, connection, cursor
from ..keyboards import get_button


def KeyboardDistr():
    colorDaily = "negative"
    cursor.execute("SELECT distr FROM users WHERE ID_VK = " + str(MessageSettings.getId()))
    distr = int((cursor.fetchone())[0])
    print(distr)
    if distr > -1:
        colorDaily = "positive"
    keyboard = {
        "one_time": False,
        "buttons": [
            [get_button(label="Ежедневная рассылка", color=colorDaily,
                        payload={'button': 'distrEveryday', "action": str(distr)})],
            [get_button(label="Назад", color="primary")]
        ]

    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard


async def info():
    print("distrEveryday")
    id = MessageSettings.getId()
    sost = int(MessageSettings.payload["action"])
    if sost == -1:
        cursor.execute("UPDATE users SET distr = 0 WHERE ID_VK = " + str(id))
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Включено",
                               keyboard=KeyboardDistr(),
                               random_id=random.randint(1, 2147483647))
    elif sost == 0:
        cursor.execute("UPDATE users SET distr = -1 WHERE ID_VK = " + str(id))
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Выключено",
                               keyboard=KeyboardDistr(),
                               random_id=random.randint(1, 2147483647))

    connection.commit()

    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "distrEveryday"
