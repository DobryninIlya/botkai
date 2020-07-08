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
    group = UserParams.groupId
    id = MessageSettings.id
    sql = "SELECT * FROM Users WHERE" + " Groupp = " + str(group)
    cursor.execute(sql)
    result = cursor.fetchall()
    connection.close()
    members = "Список группы: \n"
    i = 1
    print(len(result))
    for elem in result:
        if elem[0] < 2000000000:
            admin = "\n"
            print(elem[4], elem[1])
            if (int)(elem[4]) > 90:
                admin = " (Разработчик)\n"
            elif (int)(elem[4]) > 4:
                admin = " (Администратор)\n"
            members += str(i) + ". " + "@id" + str(elem[0]) + " (" + (str(elem[1])).rstrip() + ")" + str(admin)
            i+=1
    vk.method("messages.send", {"peer_id": id, "message": members , "random_id": random.randint(1, 2147483647)})
    

    return "ok"




command = command_class.Command()




command.keys = ['моя группа', 'список группы']
command.desciption = 'отображение списка заданий'
command.process = info
command.payload = "groupmembers"