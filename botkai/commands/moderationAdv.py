import classes as command_class
import vk_api
import random
from keyboards import GetModerAdvButton
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3
import psycopg2
import traceback
from main import vk, cursorR, conn, cursor


today = datetime.date.today()
chetn = UserParams.getChetn()
BASE_URL = 'https://kai.ru/raspisanie' 



def info():
    #conn = sqlite3.connect("bot.db")
    #cursorR = conn.cursor()
    id = MessageSettings.getId()

    try:
        #sql = "INSERT INTO Status VALUES (" + str(id) + ", 100);"
        #cursorR.execute(sql)
        conn.commit()
        #conn.close()
        cursor.execute('SELECT * FROM "Adv" WHERE ischeked < 1 LIMIT 1')
        res = cursor.fetchone()
        
        vk.method("messages.send",
            {"peer_id": id, "message": "Начата модерация объявлений", "random_id": random.randint(1, 2147483647)})
        if res:
            ans = "Объявление §\n"
            ans += "\nid " + str(res[0]) + " from @id" + str(res[2])
            ans += "\n date: " + str(res[3])
            ans += "\n" + str(res[4])
            vk.method("messages.send",
                {"peer_id": id, "message": str(ans), "keyboard": GetModerAdvButton(res[0]), "random_id": random.randint(1, 2147483647)})
        else:
            vk.method("messages.send",
                {"peer_id": id, "message": "Все проверено", "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        #conn.rollback()
        vk.method("messages.send",
            {"peer_id": id, "message": "Произошла ошибка. Модерация", "random_id": random.randint(1, 2147483647)})

    return "ok"



command = command_class.Command()




command.keys = ['!moder adv', 'moder adv']
command.desciption = ''
command.process = info
command.payload = "moderadv"
command.admlevel = 4
