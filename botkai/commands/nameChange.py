from .. import classes as command_class
from ..keyboards import keyboardNull
from ..classes import vk, MessageSettings, conn, cursorR
import random



def info():
    #conn = sqlite3.connect("bot.db")
    #cursorR = conn.cursor()
    id = MessageSettings.getId()


    sql = "INSERT INTO Status VALUES (" + str(id) + ", 55);"
    cursorR.execute(sql)
    conn.commit()
    #conn.close()
    vk.method("messages.send",
            {"peer_id": MessageSettings.getPeer_id(), "message": "Введи имя в чат", "keyboard": keyboardNull, "random_id": random.randint(1, 2147483647)})
    return "ok"

command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "namechange"