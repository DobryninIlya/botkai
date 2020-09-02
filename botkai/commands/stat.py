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
    unic_groups = "\nКоличество уникальных групп с начала года: "
    cursor.execute("SELECT COUNT(DISTINCT groupreal) FROM users WHERE datechange > '2020.08.20'")
    groups_res = cursor.fetchone()[0]
    unic_groups += str(groups_res) + '\n'
    vk.method("messages.send",
                        {"peer_id": id, "message": "Число активных пользователей сегодня: " + str(len(UserParams.statUser)) + "\n" + res + unic_groups + "\n Всего обращений: " + str(MessageSettings.allCommands) + "\nВремя работы " + (str(delta))[:-7], "random_id": random.randint(1, 2147483647)})
    
      
    return "ok"



command = command_class.Command()




command.keys = ['!stat', 'stat']
command.desciption = 'статистика для админов'
command.process = info
command.payload = "statistic"
command.admlevel = 4
