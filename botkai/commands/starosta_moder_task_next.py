import random
import traceback

from .. import classes as command_class
from ..classes import vk, cursor
from ..keyboards import GetModerTaskStarosta


async def info(MessageSettings, user):
    try:
        UserID = MessageSettings.getId()
        if "callback" not in MessageSettings.buttons and False:
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message="Команда доступна только в мобильной версии сайта m.vk.com и в последней версии официального мобильного приложения.",
                                   random_id=random.randint(1, 2147483647))
            return
        groupId = user.getGroup()
        val_id = MessageSettings.payload["id"]
        pos_id = MessageSettings.payload["pos_id"]
        # message_id = MessageSettings.payload["msg_id"]
        if MessageSettings.payload["type"] == "next":
            pos_id += 1
        elif MessageSettings.payload["type"] == "prev":
            if pos_id > 0:
                pos_id -= 1
            else:
                pos_id = 0
        else:
            pos_id = 0
        sql = "SELECT * FROM Task WHERE groupid = {} LIMIT 3 OFFSET {}".format(groupId,
                                                                               0 if int(pos_id) - 1 < 0 else int(
                                                                                   pos_id) - 1)
        # print(sql)
        cursor.execute(sql)
        task = ""
        att = ""

        curs = cursor.fetchall()
        # print(curs, task)
        if len(curs) == 0:
            await vk.messages.edit(peer_id=MessageSettings.getPeer_id(),
                                   message="Задания закончились",
                                   conversation_message_id=MessageSettings.conversation_message_id)
        first = True
        second = False
        next_task_id = -1
        prev_id_task = 1
        id = -1
        content_source = ""

        for row in curs:
            if int(val_id) == 1 or len(curs) <= 1 or not pos_id:
                id = int(row[0])
                task = "❗зᴀдᴀниᴇ❗\n"
                task += str(row[4])
                idvk = "@id" + str(row[2])
                task += "\n" + idvk + " (Автор) | ID: " + str(row[0])
                att = str(row[5])
                content_source = row[7]
                first = second = False
                if len(curs) > 1:
                    next_task_id = curs[1][0]
                else:
                    next_task_id = -1
                prev_id_task = 0
                break

            if first:
                prev_id_task = int(row[0])
                # print("prev id ", prev_id_task)
                first = False
                second = True
            elif second:

                id = (int)(row[0])
                task = "❗зᴀдᴀниᴇ❗\n"
                task += str(row[4])
                idvk = "@id" + str(row[2])
                task += "\n" + idvk + " (Автор) | ID: " + str(row[0])
                att = str(row[5])
                second = False
            else:
                next_task_id = int(row[0])

        print("pos_id ", pos_id)
        print("prev id ", prev_id_task)
        print("next id ", next_task_id)
        print(task)
        await vk.messages.edit(peer_id=MessageSettings.getPeer_id(),
                               message=task,
                               keyboard=GetModerTaskStarosta(id=id, next_id=next_task_id, prev_id=prev_id_task,
                                                             pos_id=pos_id),
                               content_source=content_source,
                               attachment=att,
                               conversation_message_id=MessageSettings.conversation_message_id)

        return "ok"
    except:
        print('Ошибка:\n', traceback.format_exc())


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "next_task_starosta"
command.admlevel = 2
