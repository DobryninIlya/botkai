import classes as command_class
import vk_api
import random
from keyboards import GetDeleteTaskButton, keyboardTasks
from main import vk
import psycopg2
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3

def info():
    connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
    cursor = connection.cursor()
    UserID = MessageSettings.getId()
    sql = "SELECT * FROM Task WHERE" + " UserID = " + str(UserID)
    cursor.execute(sql)
    task = ""
    att = ""

    curs = cursor.fetchall()
    print(curs)
    connection.close()
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