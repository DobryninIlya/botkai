import json
import random

from .. import classes as command_class
from ..classes import vk, MessageSettings
from ..keyboards import keyboarddonate, get_button

keyboarddonate = {
    "one_time": False,
    "buttons": [



        [{ "action": { "type": "vkpay", "hash": "action=transfer-to-group&group_id=182372147&aid=10" }}],
        [get_button(label="Назад", color="default")]


    ]
}
keyboarddonate = json.dumps(keyboarddonate, ensure_ascii=False).encode('utf-8')
keyboarddonate = str(keyboarddonate.decode('utf-8'))

def info():

    vk.method("messages.send",
            {"peer_id": MessageSettings.getPeer_id(), "message": "Пожертвования" , "keyboard": keyboarddonate, "random_id": random.randint(1, 2147483647)})
    return "ok"

command = command_class.Command()

command.keys = ['donate', 'донат', 'пожертвования']
command.desciption = 'пожертвовать на развитие бота'
command.process = info
command.payload = "donate"
