import datetime
import random

from .. import classes as command_class
from ..classes import vk, cursor

uptime = datetime.datetime.now()


async def info(MessageSettings, user):
    id = MessageSettings.getId()
    sql = "SELECT COUNT(ID_VK) FROM Users;"
    cursor.execute(sql)
    res = "Количество зарегистрированных пользователей: " + str(cursor.fetchall()[0][0]) + '\n'

    sql = "SELECT COUNT(ID_VK) FROM Users WHERE ID_VK > 2000000000;"
    cursor.execute(sql)
    gchat = "Количество подключенных бесед: " + str(cursor.fetchall()[0][0]) + '\n'
    delta = datetime.datetime.now() - uptime
    unic_groups = "\nКоличество уникальных групп с начала года: "
    cursor.execute("SELECT COUNT(DISTINCT groupreal) FROM users WHERE 'dateChange' > '2022.08.20'")
    groups_res = cursor.fetchone()[0]
    unic_groups += str(groups_res) + '\n'
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message="Число активных пользователей сегодня: {0}\n{1}{2}\n Всего обращений: {3}\nВремя работы {4}".format(
                               str(MessageSettings.cmd_payload[0]), res, unic_groups, str(MessageSettings.cmd_payload[1]),
                               (str(delta))[:-7]),
                           random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = ['!stat', 'stat']
command.desciption = 'статистика для админов'
command.process = info
command.payload = "statistic"
command.admlevel = 4
command.role.append(2)
