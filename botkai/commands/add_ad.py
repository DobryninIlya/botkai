from .. import classes as command_class
import random
import ..keyboards
from ..classes import vk, MessageSettings, UserParams, conn, cursorR


def info():
    today = datetime.date.today()
    #conn = sqlite3.connect("bot.db")
    #cursorR = conn.cursor()
    id = MessageSettings.getId()
    if UserParams.adminLevel < -10: #убрать потом
        vk.method("messages.send",
            {"peer_id": id, "message": 'Временно недоступно.', "random_id": random.randint(1, 2147483647)})
        return "ok"
    date = str(datetime.date(today.year, today.month, today.day)  + datetime.timedelta(days=7))[5:]
    date = date.split('-')
    date = date[1] + "." + date[0]
    vk.method("messages.send",
            {"peer_id": id, "message": 'Хочешь добавить Объявление? Такое объявление отображается вместе с расписанием в соответствующий день\n Введите число, на которое запланировано объявление. Например, "' + date + '". Важно ввести именно в таком формате (без кавычек).', "keyboard" : keyboards.keyboardAddTasks, "random_id": random.randint(1, 2147483647)})
    sql = "INSERT INTO Status VALUES (" + str(id) + ", 52);"
    cursorR.execute(sql)
    conn.commit()
    #conn.close()
    return "ok"




command = command_class.Command()




command.keys = ['добавить задание']
command.desciption = 'добавить задание на определенный день'
command.process = info
command.payload = "add ad"