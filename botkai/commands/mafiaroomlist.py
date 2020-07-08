import classes as command_class
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
    sql = "SELECT * FROM mafiaRooms WHERE status = 0"
    cursorR.execute(sql)
    res = cursorR.fetchall()
    print("res = " , res)
    result = "Список доступных комнат:\n"
    for row in res:
        sql = "SELECT COUNT(*) FROM mafiaUsers WHERE room = " + str(row[0])
        print(sql)
        cursorR.execute(sql)
        countUsers = cursorR.fetchone()[0]
        result += "id " + str(row[0]) + ":: Игроков " + str(countUsers) + "/" + str(row[1]) + "\n"
    if not res:
        result = "Свободных  комнат нет. Создайте сами."
    vk.method("messages.send", {"peer_id": id, "message": result, "random_id": random.randint(1, 2147483647)})
    return "ok"




command = command_class.Command()




command.keys = ['mafiaroomlist']
command.desciption = ''
command.process = info
command.payload = "mafiaroomlist"