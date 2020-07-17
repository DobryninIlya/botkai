import classes as command_class
import vk_api
import json
import random
import datetime
import sqlite3
from main import vk, cursorR, conn
from message_class import MessageSettings
from user_class import UserParams
from keyboards import keyboardNull



def info():
    #conn = sqlite3.connect("bot.db")
    #cursorR = conn.cursor()
    id = MessageSettings.getId()


    sql = "INSERT INTO Status VALUES (" + str(id) + ", 55);"
    cursorR.execute(sql)
    conn.commit()
    #conn.close()
    vk.method("messages.send",
            {"peer_id": MessageSettings.getPeer_id(), "message": "Введи имя в чат", "keyboard": keyboardNull, "random_id": random.randint(1, 2147483647)})
    return "ok"

command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "namechange"