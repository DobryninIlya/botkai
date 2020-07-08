import command_class
import vk_api
import random
import datetime
import json
import requests
from keyboards import get_button

from main import vk
from message_class import MessageSettings
from user_class import UserParams




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