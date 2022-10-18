import datetime
import random
import traceback

from .. import classes as command_class
from .. import keyboards
from ..classes import vk, cursor


async def info(MessageSettings, user):
    try:
        today = datetime.date.today()
        id = MessageSettings.getId()
        group = user.getGroup()
        button = MessageSettings.button
        payload = MessageSettings.payload
        date = payload["date"]
        if date == "tomorrow":
            await ShowTask(id, group, datetime.date(today.year, today.month, today.day) + datetime.timedelta(days=1), MessageSettings, user)
            return "ok"
        elif date == "today":
            await ShowTask(id, group, datetime.date(today.year, today.month, today.day), MessageSettings, user)
            return "ok"
        elif date == "after":
            await ShowTask(id, group, datetime.date(today.year, today.month, today.day) + datetime.timedelta(days=2), MessageSettings, user)
            return "ok"
        elif date == "all":
            pass
        elif button == "task":
            date = payload["date"]
            await ShowTask(id, group, date, MessageSettings, user)
            return "ok"

    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())

        return "no"
    return "ok"


async def ShowTask(id, groupId, date, MessageSettings, user):
    sql = "SELECT * FROM Task WHERE" + " GroupID = " + str(groupId) + " AND Datee = '" + str(date) + "'"
    cursor.execute(sql)
    task = ""
    att = ""

    curs = cursor.fetchall()
    if len(curs) == 0:
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Заданий нет. Самое время добавить!",
                               keyboard=keyboards.keyboardTasks,
                               random_id=random.randint(1, 2147483647))

    for row in curs:
        task = "❗зᴀдᴀниᴇ❗\n"

        task += str(row[4])
        idvk = "@id" + str(row[2])
        task += "\n" + idvk + " (Автор) | ID: " + str(row[0])
        att = str(row[5])
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message=task,
                               keyboard=keyboards.getMainKeyboard(user.role),
                               content_source=row[7],
                               attachment=att,
                               random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = ['']
command.desciption = ''
command.process = info
command.payload = "task"
command.role = [1, 2, 3, 6]
