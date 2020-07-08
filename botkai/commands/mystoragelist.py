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
import datetime
from keyboards import storageMain as keyboard


def info():
    today = datetime.date.today()
    date = str(datetime.date(today.year, today.month, today.day))
    id = MessageSettings.getId()
    cursor.execute("SELECT * FROM storage WHERE (ischecked = 0 or ischecked = 1) and id_vk = " + str(id))
    re = cursor.fetchall()
    
    msg = "Список ваших файлов: \n"

    if not re:
        vk.method("messages.send",
                {"peer_id": id, "message": 'Вы не загрузили ни одного файла.',"keyboard": keyboard, "random_id": random.randint(1, 2147483647)})
        return "ok"
    for row in re:
        msg += "id " + str(row[7]) + " ~ " + (str(row[1]).rstrip())[:100] + " :: " + (str(row[3]).rstrip())[:100] + "\n"



    vk.method("messages.send",
                {"peer_id": id, "message": msg,"keyboard": keyboard, "random_id": random.randint(1, 2147483647)})


    return "ok"





command = command_class.Command()




command.keys = ['мои файлы']
command.desciption = ''
command.process = info
command.payload = "mystoragelist"
