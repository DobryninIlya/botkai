from .. import classes as command_class
import random
from ..keyboards import KeyboardProfile
from ..classes import vk, MessageSettings, connection, cursor, UserParams
import traceback
import datetime

BASE_URL = 'https://kai.ru/raspisanie' 

def info():
    groupId = UserParams.groupId

    try:
        response = requests.post( BASE_URL, data = "groupId=" + str(groupId), headers = {'Content-Type': "application/x-www-form-urlencoded"}, params = {"p_p_id":"pubStudentSchedule_WAR_publicStudentSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"}, timeout = 3)
        sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(json.dumps(response.json()), datetime.date.today(), groupId)
        cursor.execute(sql)
        connection.commit()
        message = "Расписание обновлено"
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