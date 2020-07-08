import command_class
import vk_api
import random
import keyboards
from main import vk, cursor, connection, cursorR, conn
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3
import psycopg2
import traceback
import keyboards

def info():
    
    id = MessageSettings.getId()
    cursor.execute("SELECT * FROM Users WHERE ID_VK > 2000000000")
    res = cursor.fetchall()
    result = "\n"
    for row in res:
        result += str(row[0]) + " | " + str(row[5]) + "\n"
    sql = "INSERT INTO Status VALUES (" + str(id) + ", 60);"
    cursorR.execute(sql)
    conn.commit()

    vk.method("messages.send",
                        {"peer_id": id, "message": "Введи id чата." + result, "random_id": random.randint(1, 2147483647)})

    
      
    return "ok"



command = command_class.Command()




command.keys = ["слушать чат"]
command.desciption = ''
command.process = info
command.payload = "chat"

