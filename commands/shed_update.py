import datetime
import json
import random

import requests

from .. import classes as command_class
from ..classes import vk, MessageSettings, connection, cursor, UserParams
from ..keyboards import KeyboardProfile

BASE_URL = 'https://kai.ru/raspisanie' 

def info():
    groupId = UserParams.groupId

    try:
        response = requests.post( BASE_URL, data = "groupId=" + str(groupId), headers = {'Content-Type': "application/x-www-form-urlencoded"}, params = {"p_p_id":"pubStudentSchedule_WAR_publicStudentSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"}, timeout = 20)
        assert json.dumps(response.json()), "Расписание имеет некорректную форму"
        try:
            sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(json.dumps(response.json()), datetime.date.today(), groupId)
            cursor.execute(sql)
        except:
            sql = "INSERT INTO saved_timetable VALUES('{}','{}','{}')".format(json.dumps(response.json()), datetime.date.today(), groupId)
            cursor.execute(sql)
        connection.commit()
        message = "Расписание обновлено"
        print(response.json(), groupId)
    except:
        message = "Не удалось обновить расписание"
    vk.method("messages.send",
        {"peer_id": MessageSettings.id, "message": message,"keyboard": KeyboardProfile(), "random_id": random.randint(1, 2147483647)})

    return "ok"





command = command_class.Command()




command.keys = []
command.desciption = ''
command.process = info
command.payload = "shed_update"
command.admlevel = 2