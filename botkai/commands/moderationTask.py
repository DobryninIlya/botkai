from .. import classes as command_class
from ..keyboards import GetModerAdvButton
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random



today = datetime.date.today()
chetn = UserParams.getChetn()




def info():
    #conn = sqlite3.connect("bot.db")
    #cursorR = conn.cursor()
    id = MessageSettings.getId()

    try:
        #sql = "INSERT INTO Status VALUES (" + str(id) + ", 100);"
        #cursorR.execute(sql)
        conn.commit()
        #conn.close()
        cursor.execute('SELECT * FROM Task WHERE "IsCheked" < 1 LIMIT 1')
        res = cursor.fetchone()
        
        vk.method("messages.send",
            {"peer_id": id, "message": "Начата модерация заданий", "random_id": random.randint(1, 2147483647)})
        if res:
            ans = "Задание §\n"
            ans += "\nid " + str(res[0]) + " from @id" + str(res[2])
            ans += "\n date: " + str(res[3])
            ans += "\n" + str(res[4])
            att = str(res[5])
            vk.method("messages.send",
                {"peer_id": id, "message": str(ans), "attachment": att, "keyboard": GetModerTaskButton(res[0]), "random_id": random.randint(1, 2147483647)})
        else:
            vk.method("messages.send",
                {"peer_id": id, "message": "Все проверено", "random_id": random.randint(1, 2147483647)})
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        conn.rollback()
        vk.method("messages.send",
            {"peer_id": id, "message": "Произошла ошибка. Модерация", "random_id": random.randint(1, 2147483647)})

    return "ok"



command = command_class.Command()




command.keys = ['!moder task', 'moder task']
command.desciption = ''
command.process = info
command.payload = "modertask"
command.admlevel = 4
