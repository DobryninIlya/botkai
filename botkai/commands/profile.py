import classes as command_class
import vk_api
import random
from main import vk
from message_class import MessageSettings
from keyboards import KeyboardProfile
from user_class import UserParams


def info():
    UserParams.update()
    id = MessageSettings.getPeer_id()
    message = "Профиль"
    vk.method("messages.send",
                    {"peer_id": id, "message": message, "keyboard" : KeyboardProfile(),
                        "random_id": random.randint(1, 2147483647)})

command = command_class.Command()

command.keys = ['профиль', 'настройки']
command.desciption = 'Покажу твой профиль'
command.process = info
command.payload = "profile"