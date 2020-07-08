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
    #conn = sqlite3.connect("bot.db")
    #cursorR = conn.cursor()
    id = MessageSettings.getId()
    vk.method("messages.send",
            {"peer_id": id, "message": 'Создание комнаты. Введите количество игроков от 3 до 20.', "keyboard" : keyboards.exit, "random_id": random.randint(1, 2147483647)})
    sql = "INSERT INTO Status VALUES (" + str(id) + ", 205);"
    cursorR.execute(sql)
    conn.commit()
    #conn.close()
    return "ok"





command = command_class.Command()




command.keys = ['мафия создать комнату']
command.desciption = ''
command.process = info
command.payload = "mafiaroomadd"