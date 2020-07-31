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
        sql = "SELECT * FROM Task WHERE groupid = {} LIMIT 3 OFFSET {}".format(groupId, 0 if int(val_id)-2 < 0 else int(val_id)-2)
        print(sql)
        cursor.execute(sql)
        task = ""
        att = ""

        curs = cursor.fetchall()
        print(curs, task)    
        if len(curs) == 0:
            vk.method("messages.edit", {
                "peer_id": UserID, 
                "message": "Задания закончились",
                "conversation_message_id" : MessageSettings.conversation_message_id,
                "random_id": random.randint(1, 2147483647)})
        first = True
        second = False
        next_task_id = -1
        prev_id_task = 1
        id = -1 
        for row in curs:
            if int(val_id) == 1:
                id =  (int)(row[0])
                task = "❗зᴀдᴀниᴇ❗\n"
                task += str(row[4])
                idvk = "@id" + str(row[2])
                task += "\n" + idvk + " (Автор) | ID: " + str(row[0])
                att = str(row[5])
                first = second = False
                break
                
            if first :
                prev_id_task = int(row[0])
                print("prev id ", prev_id_task)
                first = False
                second = True
            elif second:

                id =  (int)(row[0])
                task = "❗зᴀдᴀниᴇ❗\n"
                task += str(row[4])
                idvk = "@id" + str(row[2])
                task += "\n" + idvk + " (Автор) | ID: " + str(row[0])
                att = str(row[5])
                second = False
            else:
                next_task_id = int(row[0])

        print("prev id ", prev_id_task)
        print("next id ", next_task_id)


        vk.method("messages.edit", {
            "peer_id": UserID,
            "message": task , 
            "keyboard": GetModerTaskStarosta(id = id, next_id = next_task_id, prev_id = prev_id_task),
            "conversation_message_id" : MessageSettings.conversation_message_id,
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