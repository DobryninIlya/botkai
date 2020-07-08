import command_class
import vk_api
import random
import keyboards
from main import vk
from message_class import MessageSettings
from user_class import UserParams
import datetime
import sqlite3
import psycopg2
import traceback

def info():
    
    vk.method("messages.send", {"peer_id": MessageSettings.id, "message": "Сообщества - это все студенческие организации (кружки, студсоветы, фан-клубы, мероприятия). Представители таких сообществ могут находить новых 'соплеменников' и приглашать их на мероприятия прямо внутри Бота.\n&#9881; В активной разработке&#9881;", "random_id": random.randint(1, 2147483647)})

    return "ok"


command = command_class.Command()




command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "community"
