from .. import classes as command_class
from .. import keyboards
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random
import datetime
import traceback

def info():

    try:
        today = datetime.date.today()
        id = MessageSettings.getId()
        group = UserParams.getGroup()
        button = MessageSettings.button
        payload = MessageSettings.payload
        date = payload["date"]
        print(date, payload)
        if date == "tomorrow":
            ShowTask(id, group, datetime.date(today.year, today.month, today.day)  + datetime.timedelta(days=1))
            return "ok"
        elif date == "today":
            ShowTask(id, group, datetime.date(today.year, today.month, today.day))
            return "ok"
        elif date == "after":
            ShowTask(id, group, datetime.date(today.year, today.month, today.day)  + datetime.timedelta(days=2))
            return "ok"
        elif date == "all":
            pass
        elif button == "task":
            date = payload["date"]
            ShowTask(id, group, date)
            return "ok"

    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
       

        return "no" 
    return "ok"


def ShowTask(id, groupId, date):



    sql="SELECT * FROM Task WHERE" + " GroupID = " + str(groupId) + " AND Datee = '" + str(date) + "'"
    cursor.execute(sql)
    task = ""
    att = ""
    print("ЭТАП 1")
    curs = cursor.fetchall()
    if len(curs) == 0:
        vk.method("messages.send", {"peer_id": id, "message": "Заданий нет. Самое время добавить!" , "keyboard": keyboards.keyboardTasks, "random_id": random.randint(1, 2147483647)})
    
    for row in curs:
        print("ЭТАП 1-2")
        task = "❗зᴀдᴀниᴇ❗\n"
        print("ЭТАП 1-3")
        task += str(row[4])
        idvk = "@id" + str(row[2])
        task += "\n" + idvk + " (Автор) | ID: " + str(row[0])
        att = str(row[5])
        print("ЭТАП 2")

        print("ЭТАП 3")
        vk.method("messages.send", {"peer_id": id, "message": task , "keyboard": keyboards.getMainKeyboard(UserParams.role), "attachment" : att, "random_id": random.randint(1, 2147483647)})
        print("ЭТАП 4")
        
    return "ok"


command = command_class.Command()




command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "task"
