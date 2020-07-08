import command_class
import vk_api
import random
import keyboards
from main import vk
from message_class import MessageSettings


def info():
    id = MessageSettings.getPeer_id()
    message = "Тест"
    vk.method("messages.send",
        {"peer_id": id, "message": 'Выберите пункт меню:', "keyboard" : keyboards.keyboardTasks, "random_id": random.randint(1, 2147483647)})

command = command_class.Command()

command.keys = ["задание", "задания"]
command.desciption = 'меню заданий'
command.process = info
command.payload = "task menu"
