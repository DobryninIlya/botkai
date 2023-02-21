import datetime
import random

import aiohttp
import requests

from .. import classes as command_class
from .. import keyboards


from ..classes import vk as vk

today = datetime.date.today()

BASE_URL = 'https://kai.ru/raspisanie'
BASE_URL_STAFF = "https://kai.ru/for-staff/raspisanie"


async def info(MessageSettings, user):
    group = user.getGroup()
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=await showAllTimetable(group, user.login),
                           keyboard=keyboards.getMainKeyboard(user.role),
                           random_id=random.randint(1, 2147483647))
    return "ok"


async def showAllTimetable(groupId, login):
    async with aiohttp.ClientSession() as session:
        async with await session.post(BASE_URL_STAFF, data="prepodLogin=" + str(login),
                                      headers={'Content-Type': "application/x-www-form-urlencoded", "user-agent": "BOT RASPISANIE v.1"},
                                      params={"p_p_id": "pubLecturerSchedule_WAR_publicLecturerSchedule10",
                                              "p_p_lifecycle": "2", "p_p_resource_id": "schedule"}) as response:
            response = await response.json(content_type='text/html')
    # if str(response.status_code) != '200':
    #     return "&#9888; Возникла ошибка при подключении к серверам. \nКод ошибки: " + str(
    #         response.status_code) + " &#9888;"
    if len(response) == 0:
        return "\n&#10060;\tРасписание еще не доступно.&#10060;"
    result = ''
    res = ''
    try:
        result += "&#128204;Понедельник&#128204;\n"
        day = response[str(1)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                "group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                      elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Вторник&#128204;\n"
        day = response[str(2)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                "group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                      elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Среда&#128204;\n"
        day = response[str(3)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                "group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                      elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Четверг&#128204;\n"
        day = response[str(4)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                "group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                      elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Пятница&#128204;\n"
        day = response[str(5)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                "group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                      elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Суббота&#128204;\n"
        day = response[str(6)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                "group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                      elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."

    return result


command = command_class.Command()

command.keys = ['полностью', 'расписание полностью', 'полное расписание', 'полностью расписание']
command.desciption = 'Расписание полностью'
command.process = info
command.payload = "allprepod"
command.role = [2]
