import json
import random
from ..keyboards import exit
from .. import classes as command_class
from ..classes import vk, conn, cursorR


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }


keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="Выход", color="negative")]

    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


async def info(MessageSettings, user):
    id = MessageSettings.id
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Введите свой вопрос. Можно прикрепить медиавложения.",
                           keyboard=exit,
                           random_id=random.randint(1, 2147483647))
    sql = "INSERT INTO Status VALUES (" + str(id) + ", 58);"
    cursorR.execute(sql)
    conn.commit()

    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "feedbackcreate"
command.role = [1, 2, 3, 4, 6]
