import command_class
import vk_api
import random
from main import vk
from message_class import MessageSettings
from keyboards import keyboard


def info():

    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": "Обновлено", "keyboard" : keyboard,
                        "random_id": random.randint(1, 2147483647)})

info_command = command_class.Command()

info_command.keys = ['обновить', 'обновление']
info_command.desciption = 'получение обновления'
info_command.payload = "getupdate"
info_command.process = info
