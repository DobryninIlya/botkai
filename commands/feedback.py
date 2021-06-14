import json
import random

from .. import classes as command_class
from ..classes import vk, MessageSettings


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
    "inline": True,
    "buttons": [
        [get_button(label="Продолжить", color="positive", payload = {'button': 'feedbackcreate'})]


    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))



def info():
    id = MessageSettings.getId()
    
    vk.method("messages.send",
                        {"peer_id": id, "message": "Здесь ты можешь задать свой вопрос, предложить улучшение для бота или сообщить об ошибке. Нажми на кнопку продолжить, чтобы сделать обращение", "keyboard" : keyboard,  "random_id": random.randint(1, 2147483647)})

    return "ok"



command = command_class.Command()




command.keys = ["связь с админом"]
command.desciption = ''
command.process = info
command.payload = "feedback"
command.role = [1, 2, 3, 4, 6]

