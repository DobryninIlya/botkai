import datetime
import json
import random
import aiohttp

from .. import classes as command_class
from .. import keyboards


from ..classes import vk as vk, cursor, connection

today = datetime.date.today()
BASE_URL = 'https://kai.ru/raspisanie'


async def info(MessageSettings, user):
    id = MessageSettings.getId()
    group = user.getGroup()
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=await showAllTimetable(group, MessageSettings, user),
                           random_id=random.randint(1, 2147483647),
                           keyboard=keyboards.getMainKeyboard(user.role))
    return "ok"


async def showAllTimetable(groupId, MessageSettings, user):
    isNormal, response = await getResponse(groupId, MessageSettings, user)
    if not isNormal:
        return response
    if len(response) == 0:
        return "\n&#10060;\tРасписание еще не доступно.&#10060;"
    result = ''
    res = ''
    try:
        result += "&#128204;Понедельник&#128204;\n"
        day = response[str(1)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                                      "disciplType"][
                                                                                                                  :4] + " " + \
                      elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                      elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения.\n"
    try:
        result += "&#128204;Вторник&#128204;\n"
        day = response[str(2)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                                      "disciplType"][
                                                                                                                  :4] + " " + \
                      elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                      elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения.\n"
    try:
        result += "&#128204;Среда&#128204;\n"
        day = response[str(3)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                                      "disciplType"][
                                                                                                                  :4] + " " + \
                      elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                      elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения.\n"
    try:
        result += "&#128204;Четверг&#128204;\n"
        day = response[str(4)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                                      "disciplType"][
                                                                                                                  :4] + " " + \
                      elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                      elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения.\n"
    try:
        result += "&#128204;Пятница&#128204;\n"
        day = response[str(5)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                                      "disciplType"][
                                                                                                                  :4] + " " + \
                      elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                      elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения.\n"
    try:
        result += "&#128204;Суббота&#128204;\n"
        day = response[str(6)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                                      "disciplType"][
                                                                                                                  :4] + " " + \
                      elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                      elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения.\n"

    return result


async def getResponse(groupId, MessageSettings, user):
    if user.own_shed:
        groupId = MessageSettings.getId() + 1_000_000_000
        return await get_own_shed(groupId, MessageSettings, user)

    sql = "SELECT * FROM saved_timetable WHERE groupp = {}".format(groupId)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        try:
            async with aiohttp.ClientSession() as session:
                async with await session.post(BASE_URL, data="groupId=" + str(groupId),
                                              headers={'Content-Type': "application/x-www-form-urlencoded", "user-agent": "BOT RASPISANIE v.1"},
                                              params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                                                      "p_p_lifecycle": "2", "p_p_resource_id": "schedule"}, timeout=3) as response:
                    response = await response.json(content_type='text/html')
            sql = "INSERT INTO saved_timetable VALUES ({}, '{}', '{}')".format(groupId, datetime.date.today(),
                                                                               json.dumps(response.json()))
            cursor.execute(sql)
            connection.commit()
            return True, response.json()
        except aiohttp.ServerConnectionError as err:
            return False, "&#9888;Ошибка подключения к серверу типа ConnectionError. Вероятно, сервера КАИ были выведены из строя.&#9888;"
        except aiohttp.ServerTimeoutError as err:
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
                                                  headers={'Content-Type': "application/x-www-form-urlencoded", "user-agent": "BOT RASPISANIE v.1"},
                                                  params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                                                          "p_p_lifecycle": "2", "p_p_resource_id": "schedule"},
                                                  timeout=3) as response:
                        response = await response.json(content_type='text/html')
                assert json.dumps(response.json()), "Расписание имеет некорректную форму"
                sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(
                    json.dumps(response.json()), datetime.date.today(), groupId)
                cursor.execute(sql)
                connection.commit()
                return True, response.json()
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
                                                      headers={'Content-Type': "application/x-www-form-urlencoded", "user-agent": "BOT RASPISANIE v.1"},
                                                      params={
                                                          "p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                                                          "p_p_lifecycle": "2", "p_p_resource_id": "schedule"},
                                                      timeout=3) as response:
                            response = await response.json(content_type='text/html')
                    assert json.dumps(response.json()), "Расписание имеет некорректную форму"
                    sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(
                        json.dumps(response.json()), datetime.date.today(), groupId)
                    cursor.execute(sql)
                    connection.commit()
                    return True, response.json()
                except:
                    return True, ""
            return True, json.loads(result)

    return


async def get_own_shed(groupId, MessageSettings, user):
    try:
        sql = "SELECT shedule FROM saved_timetable WHERE groupp = {}".format(groupId)
        cursor.execute(sql)
        result = cursor.fetchone()[0]
        # print(result)
        if not result:
            user.own_shed = 0
            info(MessageSettings, user)
        else:
            return True, json.loads(result)
    except:
        return False, "\n&#9888; Вы выбрали отображать собственное расписание, загруженное из Excele таблицы. В базе отсутствует такое расписание. Чтобы это исправить - либо загрузите расписание, либо смените в профиле способ получения расписания на 'Использовать расписание группы' &#9888;\n"


command = command_class.Command()

command.keys = ['полностью', 'расписание полностью', 'полное расписание', 'полностью расписание', 'расписание']
command.desciption = 'Расписание полностью'
command.process = info
command.payload = "all"
command.role = [1, 3, 5, 6]
