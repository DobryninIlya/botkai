from .. import classes as command_class
from ..keyboards import GetDeleteTaskButton, keyboardTasks
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random


def info():
    UserID = MessageSettings.getId()
    sql = "SELECT * FROM Task WHERE" + " UserID = " + str(UserID)
    cursor.execute(sql)
    task = ""
    att = ""

    curs = cursor.fetchall()
    if len(curs) == 0:
        vk.method("messages.send", {"peer_id": UserID, "message": "Заданий нет. Самое время добавить!" , "keyboard": keyboardTasks, "random_id": random.randint(1, 2147483647)})
    
    for row in curs:
        task = "❗зᴀдᴀниᴇ❗\n"
        task += str(row[4])
        idvk = "@id" + str(row[2])
        task += "\n" + idvk + " (Автор) | ID: " + str(row[0])
        att = str(row[5])
        vk.method("messages.send", {"peer_id": UserID, "message": task , "keyboard": GetDeleteTaskButton((int)(row[0])), "attachment" : att, "random_id": random.randint(1, 2147483647)})

    return "ok"




command = command_class.Command()




command.keys = ['мои задания', 'мои задачи']
command.desciption = 'отображение списка заданий'
command.process = info
command.payload = "mytask"
command.role = [1, 2, 3, 6]