import random
import traceback

from .. import classes as command_class
from ..classes import vk, cursor


async def info(MessageSettings, user):
    try:
        group = user.groupId
        sql = "SELECT * FROM Users WHERE Groupp = {} AND role = {}".format(str(group), user.role)
        cursor.execute(sql)
        result = cursor.fetchall()
        members = "Список группы: \n"
        i = 1
        for elem in result:
            if elem[0] < 2000000000:
                admin = "\n"
                if (int)(elem[4]) > 90:
                    admin = " (🐱Разработчик)\n"
                elif (int)(elem[4]) > 4:
                    admin = " (🤡 Администратор)\n"
                elif (int)(elem[4]) == 2:
                    admin = " (🙋 Староста)\n"
                members += str(i) + ". " + "@id" + str(elem[0]) + " (" + (str(elem[1])).rstrip() + ")" + str(admin)
                i += 1
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message=members,
                               random_id=random.randint(1, 2147483647))
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())

    return "ok"


command = command_class.Command()

command.keys = ['моя группа', 'список группы']
command.desciption = 'отображение списка заданий'
command.process = info
command.payload = "groupmembers"
