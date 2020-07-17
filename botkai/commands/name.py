from .. import classes as command_class
from ..keyboards import get_button
from ..classes import vk, MessageSettings, UserParams
import random


keyboard = {
    "inline": True,
    "buttons": [
        [get_button(label="Изменить", color="positive", payload = {'button': 'namechange'})],
        [get_button(label="Назaд", color="negative", payload = {'button': 'profile'})]


    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


def info():

    vk.method("messages.send",
            {"peer_id": MessageSettings.getPeer_id(), "message": "Твое имя: " + str(UserParams.name) + "\nХочешь сменить его?", "keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
    return "ok"

command = command_class.Command()

command.keys = ['имя', 'изменить имя', 'сменить имя']
command.desciption = 'изменение имени'
command.process = info
command.payload = "name"