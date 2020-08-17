from .. import classes as command_class
from ..keyboards import keyboarddonate, get_button
from ..classes import vk, MessageSettings, UserParams
import random
import json




keyboard = {
    "inline": True,
    "buttons": [
        [get_button(label="Изменить", color="positive", payload = {'button': 'groupchange'})],
        [get_button(label="Назaд", color="negative", payload = {'button': 'profile'})]


    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

def info():
    id = MessageSettings.getId()
    group = UserParams.RealGroup
    if group == 0:
        group = "Не задано! Хочешь задать?"
    else:
        group = str(group) + " . Хочешь изменить?"
    vk.method("messages.send",
            {"peer_id": id, "message": "Твоя группа: " + str(group), "keyboard":keyboard, "random_id": random.randint(1, 2147483647)})
    return "ok"


command = command_class.Command()

command.keys = ['!группа', "группа"]
command.desciption = 'изменение группы'
command.process = info
command.payload = "group"