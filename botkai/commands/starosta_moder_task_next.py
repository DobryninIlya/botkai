from .. import classes as command_class
from ..keyboards import GetModerTaskStarosta
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random
import traceback


def info():
    try:
        UserID = MessageSettings.getId()
        if "callback" not in MessageSettings.buttons and False:
            vk.method("messages.send", {"peer_id": UserID, "message": "Команда доступна только в мобильной версии сайта m.vk.com и в последней версии официального мобильного приложения." , "random_id": random.randint(1, 2147483647)})
            return
        groupId = UserParams.getGroup()
        val_id = MessageSettings.payload["id"]
        #message_id = MessageSettings.payload["msg_id"]
        sql = "SELECT * FROM Task WHERE groupid = {} LIMIT 2 OFFSET {}".format(groupId, val_id )
        cursor.execute(sql)
        task = ""
        att = ""

        curs = cursor.fetchall()
        if len(curs) == 0:
            vk.method("messages.edit", {
                "peer_id": UserID, 
                "message": "Задания закончились",
                "conversation_message_id" : 1792, #MessageSettings.conversation_message_id,
                #"message_id" : 2058, #message_id,
                "random_id": random.randint(1, 2147483647)})
        first = True
        next_task_id = -1
        id = -1 
        for row in curs:
            if first:
                id =  (int)(row[0])
                task = "❗зᴀдᴀниᴇ❗\n"
                task += str(row[4])
                idvk = "@id" + str(row[2])
                task += "\n" + idvk + " (Автор) | ID: " + str(row[0])
                att = str(row[5])
                first = False
            else:
                next_task_id = int(row[0])

        print(curs, task)            
        vk.method("messages.edit", {
            "peer_id": UserID,
            "message": task , 
            "keyboard": GetModerTaskStarosta(id = id, next_id = next_task_id, prev_id = 0, message_id = 0),
            "conversation_message_id" : 1792, #MessageSettings.conversation_message_id,
            #"message_id" : 2058, #message_id, 
            "attachment" : att, 
            "random_id": random.randint(1, 2147483647)})

        return "ok"
    except:
        print('Ошибка:\n', traceback.format_exc())  

command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "next_task_starosta"
command.admlevel = 2