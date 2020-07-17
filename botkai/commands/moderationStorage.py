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
import keyboards
from main import vk, cursorR, conn, cursor


today = datetime.date.today()
chetn = UserParams.getChetn()
BASE_URL = 'https://kai.ru/raspisanie' 



def info():
    #conn = sqlite3.connect("bot.db")
    #cursorR = conn.cursor()
    id = MessageSettings.getId()

    try:
        
        cursor.execute('SELECT * FROM Storage WHERE ischecked = 0 LIMIT 1')
        res = cursor.fetchone()
        
        vk.method("messages.send",
            {"peer_id": id, "message": "Начата модерация хранилища", "random_id": random.randint(1, 2147483647)})
        if res:
            ans = "ХРАНИЛИЩЕ | Файл " + str(res[7]) + " §\n"
            ans += " from @id" + str(res[0]) + "\n"
            ans += "Предмет: " + str(res[1]) + "\n"
            ans += str(res[3]) + "|\n"
            ans += str(res[4])
            vk.method("messages.send",
                {"peer_id": id, "message": str(ans), "keyboard": keyboards.GetModerStorageButton(res[7]),"attachment": res[2], "random_id": random.randint(1, 2147483647)})
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




command.keys = ['!moder storage', 'moder storage']
command.desciption = ''
command.process = info
command.payload = "moderstorage"
command.admlevel = 4
