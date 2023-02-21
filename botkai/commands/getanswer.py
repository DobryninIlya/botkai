import json
import random
import traceback

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
    try:
        id = MessageSettings.id
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Введите ответ",
                               random_id=random.randint(1, 2147483647),
                               keyboard=keyboard)
        sql = "INSERT INTO Status VALUES (" + str(id) + ", 59);"
        cursorR.execute(sql)
        conn.commit()

        sql = "INSERT INTO answers VALUES (" + str(id) + "," + str(MessageSettings.payload["id"]) + ");"
        cursorR.execute(sql)
        conn.commit()
    except Exception:
        print('Ошибка:\n', traceback.format_exc())
        # pass

    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "getanswer"
command.admlevel = 90
