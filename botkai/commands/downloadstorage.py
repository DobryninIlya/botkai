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
import datetime


def info():
    
    id = MessageSettings.getId()
    
    try:
        sql = "SELECT balance FROM Users WHERE ID_VK=" + str(id) + ';'
        cursor.execute(sql)
        realAmount = cursor.fetchone()
        realAmount = realAmount[0]
        realAmount = (str(realAmount))[1:]
        amount = (int)((float)(realAmount.replace(',', '')))
        if amount >= 14:
            sql = "UPDATE Users SET balance=" + str(float(amount-14)) + " WHERE ID_VK=" + str(id) + ';'
            cursor.execute(sql)
            connection.commit()
            sql = "SELECT media_vk FROM storage WHERE id = " + MessageSettings.payload['id'] 
            cursor.execute(sql)
            res = cursor.fetchone()
            print(res)
            vk.method("messages.send",
                {"peer_id": id, "message": "Ваш файл.\n💰Баланс уменьшен на 14 монет.","attachment": str(res[0]),"keyboard": keyboards.storageMain, "random_id": random.randint(1, 2147483647)})
        else:
            vk.method("messages.send",
                {"peer_id": id, "message": "Недостаточно монет. Вы можете пополнить их через донат или загрузить какой-либо файл в Хранилище.","keyboard": keyboards.keyboarddonate, "random_id" : random.randint(1, 2147483647)})

    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        vk.method("messages.send",
            {"peer_id": id, "message": "Произошла ошибка. Модерация", "random_id": random.randint(1, 2147483647)})
    return "ok"





command = command_class.Command()




command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "downloadstorage"
