import command_class
import vk_api
import random
import datetime
import json
import requests
from keyboards import keyboardNull
import sqlite3
from main import vk, cursorR, conn
from message_class import MessageSettings
from user_class import UserParams
from keyboards import keyboardNull, keyboardAddTasks2
import traceback

today = datetime.date.today()
chetn = UserParams.getChetn()
BASE_URL = 'https://kai.ru/raspisanie' 



def info():
    #conn = sqlite3.connect("bot.db")
    #cursorR = conn.cursor()
    id = MessageSettings.getId()

    try:
        sql = "INSERT INTO Status VALUES (" + str(id) + ", 56);"
        cursorR.execute(sql)
        conn.commit()
        #conn.close()
        vk.method("messages.send",
            {"peer_id": id, "message": "Введи группу в чат", "keyboard": keyboardAddTasks2, "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        conn.rollback()
        vk.method("messages.send",
            {"peer_id": id, "message": "Произошла ошибка. Повторите позже", "random_id": random.randint(1, 2147483647)})

    return "ok"


command = command_class.Command()

command.keys = ['!группа', "группа"]
command.desciption = 'изменение группы'
command.process = info
command.payload = "groupchange"