import classes as command_class
import vk_api
import random
from keyboards import GetAdminPanel
from main import vk, connection, cursor
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3
import psycopg2
import traceback


def info():
    statUser = MessageSettings.statUser
    id = MessageSettings.getId()

    vk.method("messages.send",
                        {"peer_id": id, "message": "Apanel","keyboard": GetAdminPanel(UserParams.getAdminLevel()), "random_id": random.randint(1, 2147483647)})

    
      
    return "ok"



command = command_class.Command()




command.keys = ['apanel']
command.desciption = 'админ панель'
command.process = info
command.payload = "apanel"
command.admlevel = 4
