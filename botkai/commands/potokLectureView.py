import json
import random

from .. import classes as command_class
from ..classes import vk, MessageSettings, cursor
from ..keyboards import get_button


def KeyboardDistr():

    colorDaily = "negative"
    cursor.execute("SELECT distr FROM users WHERE ID_VK = " + str(MessageSettings.getId()))
    distr = int((cursor.fetchone())[0])
    # print(distr)
    if distr>-1:
        colorDaily = "positive"
    keyboard = {
        "one_time": False,
        "buttons": [
            [get_button(label="Ежедневная рассылка", color=colorDaily, payload = {'button': 'distrEveryday', "action" : str(distr)})],
                [get_button(label="Назад", color="primary")]
            ]
            
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))

    return keyboard


def info():

    
    sql = "SELECT potok_lecture FROM users WHERE id_vk = {id_vk}".format(id_vk = MessageSettings.getId())
    cursor.execute(sql)
    res = cursor.fetchone()[0]

    if res:
        cursor.execute("UPDATE users SET potok_lecture = {} WHERE ID_VK = {}".format(False, MessageSettings.getId()))
        vk.method("messages.send",
                        {"peer_id": MessageSettings.getId(), "message": "Отображение потоковых лекций выключено", "random_id": random.randint(1, 2147483647)})
    else:
        cursor.execute("UPDATE users SET potok_lecture = {} WHERE ID_VK = {}".format(True, MessageSettings.getId()))
        vk.method("messages.send",
                        {"peer_id": MessageSettings.getId(), "message": "Отображение потоковых лекций включено", "random_id": random.randint(1, 2147483647)})


    return "ok"



command = command_class.Command()




command.keys = ["поток","потоковая лекция"]
command.desciption = 'включить или отключить отображение дистанционных лекций'
command.process = info
command.payload = "potokLectureSettings"

