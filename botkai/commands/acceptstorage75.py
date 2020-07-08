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
    today = datetime.date.today()
    date = str(datetime.date(today.year, today.month, today.day))
    id = MessageSettings.getId()
    idMedia = MessageSettings.payload["id"]
    print(MessageSettings.payload, idMedia)
    cursor.execute("UPDATE storage SET ischecked = 1, datecheck = '" + date + "', chekedby = " + str(id) + " WHERE id = " + str(idMedia))
    connection.commit()
    cursor.execute("SELECT * FROM storage WHERE id = " + str(idMedia))
    re = cursor.fetchone()
    try:
        idUser = re[0]
    except TypeError:
        vk.method("messages.send",
                {"peer_id": id, "message": "Все проверено", "random_id": random.randint(1, 2147483647)})
    vk.method("messages.send",
                {"peer_id": idUser, "message": "Файл #" + str(idMedia) + " одобрен и опубликован. Вам начислено 150 донат очков.", "random_id": random.randint(1, 2147483647)})
    sql = "SELECT balance FROM Users WHERE ID_VK=" + str(idUser) + ';'
    cursor.execute(sql)
    realAmount = cursor.fetchone()
    realAmount = realAmount[0]
    realAmount = (str(realAmount))[1:]
    amount = 150 #75
    amount = (float)(realAmount.replace(',', '')) + (float)(amount)
    #print("last" + str(amount))
    sql = "UPDATE Users SET balance=" + str(amount) + " WHERE ID_VK=" + str(idUser) + ';'
    cursor.execute(sql)
    try:
        
        cursor.execute('SELECT * FROM Storage WHERE ischecked = 0 LIMIT 1')
        res = cursor.fetchone()
       
        if res:
            ans = "ХРАНИЛИЩЕ | Файл " + str(res[7]) + " §\n"
            ans += " from @id" + str(res[0]) + "\n"
            ans += "Предмет:" + str(res[1]) + "\n"
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




command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "acceptstorage75"
