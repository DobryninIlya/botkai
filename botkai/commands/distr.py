import classes as command_class
import vk_api
import random
import keyboards
from main import vk, cursor, connection
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3
import psycopg2
import traceback
import keyboards

def info():
    
    id = MessageSettings.getId()
    
    vk.method("messages.send",
                        {"peer_id": id, "message": "Управление подписками происходит в профиле.","keyboard" : keyboards.KeyboardProfile(), "random_id": random.randint(1, 2147483647)})

    
      
    return "ok"



command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "distr"

