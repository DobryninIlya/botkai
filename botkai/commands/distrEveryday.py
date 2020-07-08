import command_class
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
import json


def KeyboardDistr():

    colorDaily = "negative"
    cursor.execute("SELECT distr FROM users WHERE ID_VK = " + str(MessageSettings.getId()))
    distr = int((cursor.fetchone())[0])
    print(distr)
    if distr>-1:
        colorDaily = "positive"
    keyboard = {
        "one_time": False,
        "buttons": [
            [keyboards.get_button(label="Ежедневная рассылка", color=colorDaily, payload = {'button': 'distrEveryday', "action" : str(distr)})],
                [keyboards.get_button(label="Назад", color="primary")]
            ]
            
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard


def info():
    print("distrEveryday")
    id = MessageSettings.getId()
    sost = int(MessageSettings.payload["action"])
    if sost==-1:
        cursor.execute("UPDATE users SET distr = 0 WHERE ID_VK = " + str(id))
        vk.method("messages.send",
                        {"peer_id": id, "message": "Включено","keyboard" : KeyboardDistr(), "random_id": random.randint(1, 2147483647)})
    elif sost == 0:
        cursor.execute("UPDATE users SET distr = -1 WHERE ID_VK = " + str(id))
        vk.method("messages.send",
                        {"peer_id": id, "message": "Выключено","keyboard" : KeyboardDistr(), "random_id": random.randint(1, 2147483647)})
    
    connection.commit()
    
      
    return "ok"



command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "distrEveryday"

