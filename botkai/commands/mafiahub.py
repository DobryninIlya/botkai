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
    vk.method("messages.send",
            {"peer_id": id, "message": 'Карточная игра Мафия', "keyboard" : keyboards.mafiahub, "random_id": random.randint(1, 2147483647)})
    
    return "ok"




command = command_class.Command()




command.keys = ['мафия']
command.desciption = ''
command.process = info
command.payload = "mafiahub"