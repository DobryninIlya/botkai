from .. import classes as command_class
import random
import aiohttp
from ..classes import vk as vk


import traceback
import datetime

today = datetime.date.today()

BASE_URL = 'https://kai.ru/raspisanie'


async def info(MessageSettings, user):
    today = datetime.date.today()
    date = str(datetime.date(today.year, today.month, today.day) + datetime.timedelta(days=1))
    group = user.getGroup()
    id = MessageSettings.getId()

    try:
        Timetable = await showTimetable(group)
        if Timetable:
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message="Расписание экзаменов:\n" + Timetable,
                                   random_id=random.randint(1, 2147483647))
        else:
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message="Расписание экзаменов недоступно.",
                                   random_id=random.randint(1, 2147483647))
    except TypeError as E:
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Расписание экзаменов недоступно.",
                               random_id=random.randint(1, 2147483647))
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Расписание экзаменов недоступно.",
                               random_id=random.randint(1, 2147483647))


    return "ok"


async def showTimetable(groupId):
    try:
        async with aiohttp.ClientSession() as session:
            async with await session.post(BASE_URL, data="groupId=" + str(groupId),
                                          headers={'Content-Type': "application/x-www-form-urlencoded"},
                                          params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                                                  "p_p_lifecycle": "2", "p_p_resource_id": "examSchedule"},
                                          timeout=7) as response:
                response = await response.json()
        print("TEST")
        print("Response: ", response.status_code)
        if str(response.status_code) != '200':
            return "&#9888; Возникла ошибка при подключении к серверам. \nКод ошибки: " + str(
                response.status_code) + " &#9888;"
        if len(response) == 0:
            return "\n&#10060;\tНет элементов для отображения.&#10060;"

        result = ''
        for elem in response:
            result += str(chr(10148)) + (elem["examDate"]).lstrip().rstrip() + " " + (
            elem["examTime"]).lstrip().rstrip() + " " + (elem["disciplName"]).lstrip().rstrip() + " " + (
                      elem["audNum"]).lstrip().rstrip() + " ауд. " + (elem["buildNum"]).lstrip().rstrip() + " зд. \n"
        return result
    except ConnectionError as err:
        return False, "&#9888;Ошибка подключения к серверу типа ConnectionError. Вероятно, сервера КАИ были выведены из строя.&#9888;"
    except aiohttp.ServerTimeoutError as err:
        return False, "&#9888;Ошибка подключения к серверу типа Timeout. Вероятно, сервера КАИ перегружены.&#9888;"
    except:
        return False, ""


command = command_class.Command()

command.keys = ['экзамены', 'расписание экзаменов', 'exams']
command.desciption = 'Расписание экзаменов'
command.process = info
command.payload = "exams"
command.role = [1, 3]
