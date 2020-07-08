import command_class
import vk_api
import random
import keyboards
from main import vk, cursorR, conn
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3

def info():
    
    id = MessageSettings.getId()
    vk.method("messages.send",
            {"peer_id": id, "message": 'Введите ID комнаты, к которой хотите подключиться', "keyboard" : keyboards.exit, "random_id": random.randint(1, 2147483647)})
    sql = "INSERT INTO Status VALUES (" + str(id) + ", 206);"
    cursorR.execute(sql)
    conn.commit()
    return "ok"




command = command_class.Command()




command.keys = ['мафия подключиться']
command.desciption = ''
command.process = info
command.payload = "mafiainvite"