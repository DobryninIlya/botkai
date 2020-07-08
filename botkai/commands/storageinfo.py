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
                        {"peer_id": id, "message": "Хранилище - это сборник всех файлов, которые могут пригодиться в учебе в КНИТУ-КАИ. Его формируют сами студенты.\n vk.com/@botraspisanie-hranilische","attachment": "https://vk.com/@botraspisanie-hranilische","keyboard" : keyboards.storageMain, "random_id": random.randint(1, 2147483647)})

    
      
    return "ok"



command = command_class.Command()




command.keys = ["что такое хранилище", 'хранилище']
command.desciption = ''
command.process = info
command.payload = "storageinfo"

