from .. import classes as command_class
import random
import json
from ..classes import vk, MessageSettings, UserParams, connection, cursor
from ..keyboards import get_button


def KeyboardDistr():

    colorDaily = "negative"
    cursor.execute("SELECT distr FROM users WHERE ID_VK = " + str(MessageSettings.getId()))
    distr = int((cursor.fetchone())[0])
    print(distr)
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
    # print("distrEveryday")
    # id = MessageSettings.getId()
    # sost = int(MessageSettings.payload["action"])
    # if sost==-1:
    #     cursor.execute("UPDATE users SET distr = 0 WHERE ID_VK = " + str(id))
    #     vk.method("messages.send",
    #                     {"peer_id": id, "message": "Включено","keyboard" : KeyboardDistr(), "random_id": random.randint(1, 2147483647)})
    # elif sost == 0:
    #     cursor.execute("UPDATE users SET distr = -1 WHERE ID_VK = " + str(id))
    #     vk.method("messages.send",
    #                     {"peer_id": id, "message": "Выключено","keyboard" : KeyboardDistr(), "random_id": random.randint(1, 2147483647)})
    
    # connection.commit()
    
    sql = "SELECT 'potokLecture' FROM users WHERE id_vk = {id_vk}".format(id_vk = MessageSettings.getId())
    cursor.execute(sql)
    res = cursor.fetchone()[0]

    if res:
        cursor.execute("UPDATE users SET potokLecture = False WHERE ID_VK = " + str(MessageSettings.getId()))
        vk.method("messages.send",
                        {"peer_id": id, "message": "Отображение потоковых лекций выключено", "random_id": random.randint(1, 2147483647)})
    else:
        cursor.execute("UPDATE users SET potokLecture = True WHERE ID_VK = " + str(MessageSettings.getId()))
        vk.method("messages.send",
                        {"peer_id": id, "message": "Отображение потоковых лекций включено", "random_id": random.randint(1, 2147483647)})


    return "ok"



command = command_class.Command()




command.keys = ["потоковая лекция"]
command.desciption = ''
command.process = info
command.payload = "potokLectureSettings"

