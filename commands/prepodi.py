import datetime
import json
import random

import aiohttp
import requests

from .. import classes as command_class

from .. classes import cursor, connection
from ..classes import vk as vk
from ..keyboards import getMainKeyboard

BASE_URL = 'https://kai.ru/raspisanie'
prepodList = []


async def info(MessageSettings, user):
    prepodList = await GetPrepodList(MessageSettings, user)
    if not len(prepodList):
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="\n&#10060;\tРасписание еще не доступно.&#10060;",
                               keyboard=getMainKeyboard(user.role),
                               random_id=random.randint(1, 2147483647))
        return "ok"
    try:
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message=prepodList,
                               keyboard=getMainKeyboard(user.role),
                               random_id=random.randint(1, 2147483647))
    except:
        st = "&#128104;&#8205;&#127979;"
        pos = prepodList[2400:].rfind(st)
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message=prepodList[:pos],
                               keyboard=getMainKeyboard(user.role),
                               random_id=random.randint(1, 2147483647))
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message=prepodList[pos:],
                               keyboard=getMainKeyboard(user.role),
                               random_id=random.randint(1, 2147483647))
    return "ok"


class Prepodi:
    def __init__(self):
        self.disciplType = ""
        self.disciplName = ""
        self.prepodName = ""


async def getResponse(groupId, MessageSettings, user):
    today = datetime.date.today()
    if user.own_shed:
        groupId = MessageSettings.getId() + 1_000_000_000
        return await get_own_shed(groupId, user)

    sql = "SELECT * FROM saved_timetable WHERE groupp = {}".format(groupId)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        try:
            async with aiohttp.ClientSession() as session:
                async with await session.post(BASE_URL, data="groupId=" + str(groupId),
                                              headers={'Content-Type': "application/x-www-form-urlencoded"},
                                              params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                                                      "p_p_lifecycle": "2", "p_p_resource_id": "schedule"},
                                              timeout=3) as response:
                    response = await response.json(content_type='text/html')

            sql = "INSERT INTO saved_timetable VALUES ({}, '{}', '{}')".format(groupId, datetime.date.today(),
                                                                               json.dumps(response))
            cursor.execute(sql)
            connection.commit()
            return True, response
        except ConnectionError as err:
            return False, "&#9888;Ошибка подключения к серверу типа ConnectionError. Вероятно, сервера КАИ были выведены из строя.&#9888;"
        except requests.exceptions.Timeout as err:
            return False, "&#9888;Ошибка подключения к серверу типа Timeout. Вероятно, сервера КАИ перегружены.&#9888;"
        except:
            return False, ""

    else:
        date_update = result[1]
        timetable = result[2]
        if date_update + datetime.timedelta(days=2) < today:
            try:
                async with aiohttp.ClientSession() as session:
                    async with await session.post(BASE_URL, data="groupId=" + str(groupId),
                                                  headers={'Content-Type': "application/x-www-form-urlencoded"},
                                                  params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                                                          "p_p_lifecycle": "2", "p_p_resource_id": "schedule"},
                                                  timeout=3) as response:
                        response = await response.json(content_type='text/html')
                assert json.dumps(response), "Расписание имеет некорректную форму"
                sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(
                    json.dumps(response), datetime.date.today(), groupId)
                cursor.execute(sql)
                connection.commit()
                return True, response
            except:
                sql = "SELECT shedule FROM saved_timetable WHERE groupp = {}".format(groupId)
                cursor.execute(sql)
                result = cursor.fetchone()[0]
                return True, json.loads(result)
        else:
            sql = "SELECT shedule FROM saved_timetable WHERE groupp = {}".format(groupId)
            cursor.execute(sql)
            result = cursor.fetchone()[0]
            if len(result) < 10:
                try:
                    async with aiohttp.ClientSession() as session:
                        async with await session.post(BASE_URL, data="groupId=" + str(groupId),
                                                      headers={'Content-Type': "application/x-www-form-urlencoded"},
                                                      params={
                                                          "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                                                          "p_p_lifecycle": "2", "p_p_resource_id": "schedule"},
                                                      timeout=3) as response:
                            response = await response.json(content_type='text/html')
                    assert json.dumps(response), "Расписание имеет некорректную форму"
                    sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(
                        json.dumps(response), datetime.date.today(), groupId)
                    cursor.execute(sql)
                    connection.commit()
                    return True, response
                except:
                    return True, ""
            return True, json.loads(result)

    return


async def get_own_shed(groupId, user):
    try:
        sql = "SELECT shedule FROM saved_timetable WHERE groupp = {}".format(groupId)
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        # print(result)
        if not result:
            user.own_shed = 0
            info()
        else:
            return True, json.loads(result)
    except:
        return False, "\n&#9888; Вы выбрали отображать собственное расписание, загруженное из Excele таблицы. В базе отсутствует такое расписание. Чтобы это исправить - либо загрузите расписание, либо смените в профиле способ получения расписания на 'Использовать расписание группы' &#9888;\n"


async def GetPrepodList(MessageSettings, user):
    prepodList.clear()
    resultList = []
    groupId = user.getGroup()
    isNormal, response = await getResponse(groupId, MessageSettings, user)
    if not isNormal:
        return response
    if len(response) == 0:
        return "\n&#10060;\tРасписание еще не доступно.&#10060;"
    result = ''
    for key in response:
        for elem in response[key]:
            Prepod = Prepodi()
            Prepod.disciplName = elem["disciplName"]
            Prepod.disciplType = elem["disciplType"]
            Prepod.prepodName = elem["prepodName"]
            if elem["prepodName"].rstrip() == "":
                Prepod.prepodName = ":не-задан:"
            prepodList.append(Prepod)
    prepodList.sort(key=lambda Prepodi: Prepodi.disciplName)
    i = 0
    for prepod in prepodList:
        disciplType = []
        disciplType.append(prepod.disciplType)
        try:
            while prepod.prepodName == prepodList[i + 1].prepodName:
                if prepodList[i + 1].disciplType not in disciplType:
                    disciplType.append(prepodList[i + 1].disciplType)
                prepodList.pop(i)
        except:
            pass
        i += 1
        if disciplType:
            st = ""
            for discipl in disciplType:
                st += str(discipl).rstrip() + ", "
            st = st[:-2]

            prepod.disciplType = st
        res = "&#128104;&#8205;&#127979;[" + str(prepod.disciplType) + "] " + (
            str(prepod.disciplName)).rstrip() + " \n" + ((str(prepod.prepodName)).rstrip()).title()
        if res not in resultList:
            resultList.append(res)

    for row in resultList:
        result += "\n---------------------------------------------------\n" + row
    del Prepod
    return result[len("----------------------------------------------------"):]


command = command_class.Command()

command.keys = ['преподы', 'преподаватели', '!преподы', 'учителя']
command.desciption = 'список преподавателей и дисциплин'
command.process = info
command.payload = "prepod"
command.role = [1, 2, 3, 6]
