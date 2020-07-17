from .. import classes as command_class
import random
from ..keyboards import KeyboardProfile, get_button
from ..classes import vk, MessageSettings, connection, cursor
import json

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
    
    id = MessageSettings.getId()
    
    vk.method("messages.send",
                        {"peer_id": id, "message": "Текущие рассылки","keyboard" : KeyboardDistr(), "random_id": random.randint(1, 2147483647)})

    
      
    return "ok"



command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "distrMenu"

