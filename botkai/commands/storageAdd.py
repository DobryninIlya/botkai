import classes as command_class
import vk_api
import json
import random
import datetime
import sqlite3
from main import vk, cursorR, conn
from message_class import MessageSettings
from user_class import UserParams
from keyboards import exit as keyboard



def info():
    #conn = sqlite3.connect("bot.db")
    #cursorR = conn.cursor()
    id = MessageSettings.getId()
    
    sql = "INSERT INTO Status VALUES (" + str(id) + ", 180);"
    cursorR.execute(sql)
    conn.commit()
    #conn.close()
    vk.method("messages.send",
            {"peer_id": MessageSettings.getPeer_id(), "message": "Процедура добавления файла: \n1. Прикрепить файлы во вложении, \n2. Ввести полное правильное название предмета, \n3. Установить заголовок (краткое название файла: л.р, учебник, билеты, вопросы к экз. ), \n4. Подробное описание файла\n5. Подтвердить отправку.\n...[!] Загрузите ответным сообщением файл ...", "keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
    return "ok"

command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "storageadd"