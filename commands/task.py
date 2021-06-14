import datetime
import random
import traceback

from .. import classes as command_class
from .. import keyboards
from ..classes import vk, MessageSettings, UserParams, cursor


def info():

    try:
        today = datetime.date.today()
        id = MessageSettings.getId()
        group = UserParams.getGroup()
        button = MessageSettings.button
        payload = MessageSettings.payload
        date = payload["date"]
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

    curs = cursor.fetchall()
    if len(curs) == 0:
        vk.method("messages.send", {"peer_id": id, "message": "Заданий нет. Самое время добавить!" , "keyboard": keyboards.keyboardTasks, "random_id": random.randint(1, 2147483647)})
    
    for row in curs:

        task = "❗зᴀдᴀниᴇ❗\n"

        task += str(row[4])
        idvk = "@id" + str(row[2])
        task += "\n" + idvk + " (Автор) | ID: " + str(row[0])
        att = str(row[5])

        vk.method("messages.send", {"peer_id": id, "message": task , "keyboard": keyboards.getMainKeyboard(UserParams.role),"content_source": row[7], "attachment" : att, "random_id": random.randint(1, 2147483647)})

        
    return "ok"


command = command_class.Command()




command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "task"
command.role = [1, 2, 3, 6]
