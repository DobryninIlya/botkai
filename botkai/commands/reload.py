import command_class
import vk_api
import random
import keyboards
from main import vk, uptime
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3
import psycopg2
import traceback
import sys

def info():
    statUser = MessageSettings.statUser
    id = MessageSettings.getId()

    vk.method("messages.send",
                        {"peer_id": id, "message": "Перезагрузка", "random_id": random.randint(1, 2147483647)})
    sys.exit(0)
    
      
    return "ok"



command = command_class.Command()




command.keys = ['reload']
command.desciption = 'рестарт'
command.process = info
command.payload = "reload"
command.admlevel = 90
