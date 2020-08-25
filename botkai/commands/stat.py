from .. import classes as command_class
from ..keyboards import GetDeleteTaskButton, keyboardTasks
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random
import datetime

uptime = datetime.datetime.now()

def info():
    id = MessageSettings.getId()
    sql = "SELECT COUNT(ID_VK) FROM Users;"
    cursor.execute(sql)
    res = "Количество зарегистрированных пользователей: " + str(cursor.fetchall()[0][0]) + '\n'
                    
    sql = "SELECT COUNT(ID_VK) FROM Users WHERE ID_VK > 2000000000;"
    cursor.execute(sql)
    gchat = "Количество подключенных бесед: " + str(cursor.fetchall()[0][0]) + '\n'
    delta = datetime.datetime.now() - uptime
    print(MessageSettings.statUser)
    vk.method("messages.send",
                        {"peer_id": id, "message": "Число активных пользователей сегодня: " + str(UserParams.statUser) + "\n" + res + gchat + "\n Всего обращений: " + str(MessageSettings.allCommands) + "\nВремя работы " + str(delta), "random_id": random.randint(1, 2147483647)})
    connection.close()
    
      
    return "ok"



command = command_class.Command()




command.keys = ['!stat', 'stat']
command.desciption = 'статистика для админов'
command.process = info
command.payload = "statistic"
command.admlevel = 4
