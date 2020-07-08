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
import json


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }



keyboard = {
    "one_time": False,
    "buttons": [
        [get_button(label="Выход", color="negative")]


    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

def info():

    id = MessageSettings.id
    vk.method("messages.send",
                        {"peer_id": id, "message": "Введите ответ", "keyboard" : keyboard,  "random_id": random.randint(1, 2147483647)})
    sql = "INSERT INTO Status VALUES (" + str(id) + ", 59);"
    cursorR.execute(sql)
    conn.commit()
    try:
        sql = "INSERT INTO answers VALUES (" + str(id) + "," + str(MessageSettings.payload["id"]) + ");"
        print(sql)
        cursorR.execute(sql)
        conn.commit()
    except Exception:
        pass
    
      
    return "ok"



command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "getanswer"
command.admlevel = 90
