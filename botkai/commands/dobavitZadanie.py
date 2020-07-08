import command_class
import vk_api
import random
import keyboards
from main import vk, cursorR, conn
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3

def info():
    today = datetime.date.today()
    #conn = sqlite3.connect("bot.db")
    #cursorR = conn.cursor()
    id = MessageSettings.getId()
    if UserParams.adminLevel < -10: #убрать потом
        vk.method("messages.send",
            {"peer_id": id, "message": 'Временно недоступно.', "random_id": random.randint(1, 2147483647)})
        return "ok"
    date = str(datetime.date(today.year, today.month, today.day)  + datetime.timedelta(days=7))[5:]
    date = date.split('-')
    date = date[1] + "." + date[0]
    vk.method("messages.send",
            {"peer_id": id, "message": 'Хочешь добавить задание? Такое задание видят все участники группы. \n Введите число, на которое запланировано задание. Например, "' + date + '". Важно ввести именно в таком формате (без кавычек).', "keyboard" : keyboards.keyboardAddTasks, "random_id": random.randint(1, 2147483647)})
    sql = "INSERT INTO Status VALUES (" + str(id) + ", 50);"
    cursorR.execute(sql)
    conn.commit()
    #conn.close()
    return "ok"




command = command_class.Command()




command.keys = ['добавить задание']
command.desciption = 'добавить задание на определенный день'
command.process = info
command.payload = "add task"