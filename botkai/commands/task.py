import classes as command_class
import vk_api
import random
import keyboards
from main import vk
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3
import psycopg2
import traceback

def info():
    connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
    cursor = connection.cursor()
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
            connection.close()
            return "ok"
        elif date == "today":
            ShowTask(id, group, datetime.date(today.year, today.month, today.day))
            connection.close()
            return "ok"
        elif date == "after":
            connection.close()
            ShowTask(id, group, datetime.date(today.year, today.month, today.day)  + datetime.timedelta(days=2))
            return "ok"
        elif date == "all":
            connection.close()
            pass
        elif button == "task":
            date = payload["date"]
            connection.close()
            ShowTask(id, group, date)
            return "ok"
        connection.close()
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
       

        return "no" 
    return "ok"


def ShowTask(id, groupId, date):
    connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
    cursor = connection.cursor()


    sql="SELECT * FROM Task WHERE" + " GroupID = " + str(groupId) + " AND Datee = '" + str(date) + "'"
    cursor.execute(sql)
    task = ""
    att = ""
    print("ЭТАП 1")
    curs = cursor.fetchall()
    connection.close()
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
        vk.method("messages.send", {"peer_id": id, "message": task , "keyboard": keyboards.keyboard, "attachment" : att, "random_id": random.randint(1, 2147483647)})
        print("ЭТАП 4")
        
    return "ok"


command = command_class.Command()




command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "task"
