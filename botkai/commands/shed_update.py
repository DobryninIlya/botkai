import datetime
import json
import random

import aiohttp
import requests

from .. import classes as command_class
from ..classes import vk, MessageSettings, connection, cursor, UserParams
from ..keyboards import KeyboardProfile

BASE_URL = 'https://kai.ru/raspisanie'


async def info():
    groupId = UserParams.groupId

    try:
        async with aiohttp.ClientSession() as session:
            async with await session.post(BASE_URL, data="groupId=" + str(groupId),
                                 headers={'Content-Type': "application/x-www-form-urlencoded"},
                                 params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                                         "p_p_lifecycle": "2", "p_p_resource_id": "schedule"}, timeout=20) as response:
                response = await response.json(content_type='text/html')

        try:
            sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(
                json.dumps(response), datetime.date.today(), groupId)
            cursor.execute(sql)
        except:
            sql = "INSERT INTO saved_timetable VALUES('{}','{}','{}')".format(json.dumps(response),
                                                                              datetime.date.today(), groupId)
            cursor.execute(sql)
        connection.commit()
        message = "Расписание обновлено"
    except:
        message = "Не удалось обновить расписание"
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=message,
                           keyboard=KeyboardProfile(),
                           random_id=random.randint(1, 2147483647))

    return "ok"


command = command_class.Command()

command.keys = []
command.desciption = ''
command.process = info
command.payload = "shed_update"
command.admlevel = 2
