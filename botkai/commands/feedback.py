import classes as command_class
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
import json


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }



keyboard = {
    "inline": True,
    "buttons": [
        [get_button(label="Продолжить", color="positive", payload = {'button': 'feedbackcreate'})]


    ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))



def info():
    statUser = MessageSettings.statUser
    id = MessageSettings.getId()
    connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
    cursor = connection.cursor()
    
    vk.method("messages.send",
                        {"peer_id": id, "message": "Здесь ты можешь задать свой вопрос, предложить улучшение для бота или сообщить об ошибке. Нажми на кнопку продолжить, чтобы сделать обращение", "keyboard" : keyboard,  "random_id": random.randint(1, 2147483647)})
    connection.close()
    
      
    return "ok"



command = command_class.Command()




command.keys = ["обратная связь"]
command.desciption = ''
command.process = info
command.payload = "feedback"
command.role = [1, 2, 3, 4]

