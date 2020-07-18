from .. import classes as command_class
import random
from ..keyboards import KeyboardProfile
from ..classes import vk as vk
from ..classes import MessageSettings
from ..classes import UserParams


event_data = """{
    "type": "show_snackbar",
    "text": "СОЗДАТЕЛИ CALLBACK КНОПОК СОСУТ ЧЛЕНЫ ДРУГ ДРУГУ"
  }"""

def info():
    id = MessageSettings.getPeer_id()
    message = "Профиль"
    vk.method("messages.send",
                    {"peer_id": id, "message": message, "keyboard" : KeyboardProfile(),
                        "random_id": random.randint(1, 2147483647)})
    vk.method("messages.sendMessageEventAnswer",
                    {"event_id": MessageSettings.event_id,
                    "user_id": MessageSettings.id,
                    "peer_id": MessageSettings.peer_id,
                    "event_data": event_data
                    })

command = command_class.Command()

command.keys = ['профиль', 'настройки']
command.desciption = 'Покажу твой профиль'
command.process = info
command.payload = "profile"