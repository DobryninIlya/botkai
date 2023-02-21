import json
import random

from .. import classes as command_class
from ..classes import vk
from ..keyboards import get_button

keyboard = {
    "inline": True,
    "buttons": [
        [get_button(label="Изменить", color="positive", payload = {'button': 'groupchange'})],
        [get_button(label="Назaд", color="negative", payload = {'button': 'profile'})]


    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

async def info(MessageSettings, user):
    group = user.RealGroup
    if group == 0:
        group = "Не задано! Нажми ниже, чтобы задать"
    else:
        group = str(group) + " . Хочешь изменить?"
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Твоя группа: " + str(group),
                           random_id=random.randint(1, 2147483647),
                           keyboard=keyboard)
    return "ok"


command = command_class.Command()

command.keys = ['!группа', "группа"]
command.desciption = 'изменение группы'
command.process = info
command.payload = "group"