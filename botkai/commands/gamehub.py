import classes as command_class
import vk_api
import random
import keyboards
from main import vk, cursorR, conn
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3

def info():
    today = datetime.date.today()
    id = MessageSettings.getId()
    group = UserParams.groupId
    if group != 19733:
        vk.method("messages.send",
            {"peer_id": id, "message": 'К сожалению, вы не имеете доступа к данному разделу. Мини-игры находятся на тестировании и пока не могут быть доступны всем. Следите за обновлениями', "keyboard" : keyboards.getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})
        return 'ok'
    vk.method("messages.send",
            {"peer_id": id, "message": 'Выберите из списка', "keyboard" : keyboards.gamehub, "random_id": random.randint(1, 2147483647)})
    
    return "ok"




command = command_class.Command()




command.keys = ['игры', 'игра', 'мини-игры']
command.desciption = ''
command.process = info
command.payload = "gamehub"