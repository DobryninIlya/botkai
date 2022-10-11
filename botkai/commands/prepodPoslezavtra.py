import aiohttp

from .. import classes as command_class
from .. import keyboards
from ..classes import vk, MessageSettings, UserParams
import random
import datetime
import requests
import traceback

today = datetime.date.today()
chetn = UserParams.getChetn()
BASE_URL = 'https://kai.ru/raspisanie'
BASE_URL_STAFF = "https://kai.ru/for-staff/raspisanie"


async def info():
    today = datetime.date.today()
    date = str(datetime.date(today.year, today.month, today.day) + datetime.timedelta(days=2))
    login = UserParams.login
    id = MessageSettings.getId()
    try:
        Timetable = await showTimetablePrepod(login, 2)
        if Timetable:
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message="Расписание на послезавтра:\n" + Timetable,
                                   keyboard=keyboards.getMainKeyboard(UserParams.role),
                                   random_id=random.randint(1, 2147483647))
        else:
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message="Послезавтра можно отдохнуть :)",
                                   keyboard=keyboards.getMainKeyboard(UserParams.role),
                                   random_id=random.randint(1, 2147483647))
    except Exception as E:
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Послезавтра можно отдохнуть :]",
                               keyboard=keyboards.getMainKeyboard(UserParams.role),
                               random_id=random.randint(1, 2147483647))

    return "ok"


async def showTimetablePrepod(login, tomorrow=0):
    try:
        chetn = UserParams.getChetn()
        today = datetime.date.today() + datetime.timedelta(days=tomorrow)
        async with aiohttp.ClientSession() as session:
            async with await session.post(BASE_URL_STAFF, data="prepodLogin=" + str(login),
                                          headers={'Content-Type': "application/x-www-form-urlencoded"},
                                          params={"p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
                                                  "p_p_lifecycle": "2", "p_p_resource_id": "schedule"}) as response:
                response = await response.json(content_type='text/html')
        if str(response.status_code) != '200':
            return "&#9888; Возникла ошибка при подключении к серверам. \nКод ошибки: " + str(
                response.status_code) + " &#9888;"
        if len(response) == 0:
            return "\n&#10060;\tРасписание еще не доступно.&#10060;"
        response = response[str(datetime.date(today.year, today.month, today.day).isoweekday())]
        result = ''
        now = datetime.datetime.now() + datetime.timedelta(days=tomorrow)
        month = now.month
        if month < 10:
            month = "0" + str(month)
        day = str(now.day) + "." + str(month)
        for elem in response:
            dateinstr = (str((elem["dayDate"]).rstrip())).find(day)
            # print(dateinstr)
            if (elem["dayDate"]).rstrip() == "чет" and (
                    (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148)) + elem["dayDate"][:3] + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                    "group"].rstrip() + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                          elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
            elif (elem["dayDate"]).rstrip() == "неч" and not (
                    (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148)) + elem["dayDate"][:3] + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                    "group"].rstrip() + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                          elem["buildNum"]).rstrip() + ' зд.\n'
            elif (elem["dayDate"]).rstrip() == "неч/чет" and not (
                    (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148)) + " 1&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                    "group"].rstrip() + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                          elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
            elif (elem["dayDate"]).rstrip() == "неч/чет" and (
                    (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148)) + " 2&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                    "group"].rstrip() + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                          elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
            elif (elem["dayDate"]).rstrip() == "чет/неч" and (
                    (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148)) + " 1&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                    "group"].rstrip() + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                          elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
            elif (elem["dayDate"]).rstrip() == "чет/неч" and not (
                    (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148)) + " 2&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                    "group"].rstrip() + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                          elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
            elif dateinstr != -1:
                result += str(chr(10148)) + str(day) + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                          "disciplType"][
                                                                                                      :4] + " " + elem[
                              "disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                          elem["buildNum"]).rstrip() + ' зд.\n'
            elif not ((elem["dayDate"]).rstrip() == "чет") and not ((elem["dayDate"]).rstrip() == "неч"):
                result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + \
                          elem["group"].rstrip() + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                          elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        return result
    except KeyError:
        return False
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        return False


command = command_class.Command()

command.keys = ['на послезавтра', 'расписание на послезавтра', 'послезавтра']
command.desciption = 'Расписание на завтра (с учетом четности)'
command.process = info
command.payload = "afterprepod"
command.role = [2]
