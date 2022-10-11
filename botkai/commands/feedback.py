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
        [get_button(label="Продолжить", color="positive", payload={'button': 'feedbackcreate'})]

    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


async def info():
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Здесь ты можешь задать свой вопрос, предложить улучшение для бота"
                                   " или сообщить об ошибке. Учтите, что принимаются вопросы ТОЛЬКО по вопросом, касательно работы чат-бота."
                                   "Я не отвечаю на вопросы, связанные с учебным процессом, я не знаю какая у вас группа и режим работы Здравпункта."
                                   "Не тратьте свое и мое время - воспользуйтесь гуглом google.com Нажми на кнопку продолжить, чтобы сделать обращение",
                           random_id=random.randint(1, 2147483647),
                           keyboard=keyboard)
    return "ok"


command = command_class.Command()

command.keys = ["связь с админом"]
command.desciption = ''
command.process = info
command.payload = "feedback"
command.role = [1, 2, 3, 4, 6]
