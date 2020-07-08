import classes as command_class
import vk_api
import random
import keyboards
from main import vk, cursorR, conn
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3
import psycopg2
import traceback
import datetime


def info():

    id = MessageSettings.getId()
    sql = "INSERT INTO Status VALUES (" + str(id) + ", 190);"
    cursorR.execute(sql)
    conn.commit()
    vk.method("messages.send",
                {"peer_id": id, "message": 'Введите строку для поиска',"keyboard": keyboards.exit, "random_id": random.randint(1, 2147483647)})


    return "ok"





command = command_class.Command()




command.keys = ['мои файлы']
command.desciption = ''
command.process = info
command.payload = "searchstorage"
