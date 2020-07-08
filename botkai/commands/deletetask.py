import command_class
import vk_api
import random
from keyboards import KeyboardProfile
from main import vk
import psycopg2
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3
import traceback

def info():
    connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
    cursor = connection.cursor()
    groupId = UserParams.groupId
    payload = MessageSettings.payload
    id = payload["id"]
    print(id)
    try:
        sql = "DELETE FROM Task WHERE" + " id = " + str(id) + " AND userid = " + str(MessageSettings.getId()) + ";"
        print(sql)
        cursor.execute(sql)
        connection.commit()
        connection.close()
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
    vk.method("messages.send", {"peer_id": MessageSettings.id, "message": "Удалено" , "keyboard": KeyboardProfile(), "random_id": random.randint(1, 2147483647)})
    

    return "ok"




command = command_class.Command()




command.keys = []
command.desciption = 'удаление по id'
command.process = info
command.payload = "deletetask"