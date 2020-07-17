from .. import classes as command_class
from ..keyboards import keyboardAddTasks2
from ..classes import vk, MessageSettings, UserParams, connection, cursor
import random


def info():

    group = UserParams.groupId
    id = MessageSettings.id
    sql = "SELECT * FROM Users WHERE" + " Groupp = " + str(group)
    cursor.execute(sql)
    result = cursor.fetchall()
    members = "Список группы: \n"
    i = 1
    print(len(result))
    for elem in result:
        if elem[0] < 2000000000:
            admin = "\n"
            print(elem[4], elem[1])
            if (int)(elem[4]) > 90:
                admin = " (Разработчик)\n"
            elif (int)(elem[4]) > 4:
                admin = " (Администратор)\n"
            members += str(i) + ". " + "@id" + str(elem[0]) + " (" + (str(elem[1])).rstrip() + ")" + str(admin)
            i+=1
    vk.method("messages.send", {"peer_id": id, "message": members , "random_id": random.randint(1, 2147483647)})
    

    return "ok"




command = command_class.Command()




command.keys = ['моя группа', 'список группы']
command.desciption = 'отображение списка заданий'
command.process = info
command.payload = "groupmembers"