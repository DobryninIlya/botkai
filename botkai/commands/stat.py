import command_class
import vk_api
import random
import keyboards
from main import vk, uptime
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3
import psycopg2
import traceback


def info():
    id = MessageSettings.getId()
    connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
    cursor = connection.cursor()
    sql = "SELECT COUNT(ID_VK) FROM Users;"
    cursor.execute(sql)
    res = "Количество зарегистрированных пользователей: " + str(cursor.fetchall()[0][0]) + '\n'
                    
    sql = "SELECT COUNT(ID_VK) FROM Users WHERE ID_VK > 2000000000;"
    cursor.execute(sql)
    gchat = "Количество подключенных бесед: " + str(cursor.fetchall()[0][0]) + '\n'
    delta = datetime.datetime.now() - uptime
    print(MessageSettings.statUser)
    vk.method("messages.send",
                        {"peer_id": id, "message": "Число активных пользователей сегодня: " + str(MessageSettings.statUser) + "\n" + res + gchat + "\n Всего обращений: " + str(MessageSettings.allCommands) + "\nВремя работы " + str(delta), "random_id": random.randint(1, 2147483647)})
    connection.close()
    
      
    return "ok"



command = command_class.Command()




command.keys = ['!stat', 'stat']
command.desciption = 'статистика для админов'
command.process = info
command.payload = "statistic"
command.admlevel = 4
