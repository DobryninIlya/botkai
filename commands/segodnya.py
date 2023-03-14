import datetime
import json
import random
import traceback

import aiohttp
import requests

from .. import classes as command_class


from ..classes import vk, cursor, connection
from ..keyboards import GetButtonTask

today = datetime.date.today()
BASE_URL = 'https://kai.ru/raspisanie'
frazi = ["Можно сходить в кино 😚", "Можно почитать 😚", "Можно прогуляться в лесу 😚",
         "Можно распланировать дела на неделю 😚", "Можно заняться спортом, например. 😚",
         "Можно вспомнить строчки гимна КАИ 😚", "Можно заняться чем то интересным 😚",
         "Можно встретиться с друзьями 😚"]


async def info(MessageSettings, user):
    today = datetime.date.today()
    date = str(datetime.date(today.year, today.month, today.day) + datetime.timedelta(days=0))
    group = user.getGroup()
    id = MessageSettings.getId()
    taskCount = (int)(MessageSettings.GetTaskCount(date, user.groupId))
    task = ""
    if taskCount == 0:
        task = "\n&#9993;Заданий нет"
    else:
        task = "\n&#9993;Всего " + str(taskCount) + " задания(-ий)."
    advert = MessageSettings.GetAdv(date, user.groupId)
    adv = ""
    if advert:
        adv = "\n❗ [Объявление] " + MessageSettings.GetAdv(date, user.groupId) + "\n"
    try:
        Timetable = await showTimetable(group, 0, MessageSettings, user)
        if Timetable:
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message="Расписание на сегодня:\n" + Timetable + adv + task,
                                   keyboard=GetButtonTask(date),
                                   random_id=random.randint(1, 2147483647))
        else:
            await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                                   message="Сегодня занятий нет 😎\n" + frazi[random.randint(0, len(frazi) - 1)],
                                   keyboard=GetButtonTask(date),
                                   random_id=random.randint(1, 2147483647))
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                               message="Сегодня можно отдохнуть :]",
                               keyboard=GetButtonTask(date),
                               random_id=random.randint(1, 2147483647))
    return "ok"


async def showTimetable(groupId, tomorrow=0,MessageSettings=None, user=None):
    try:
        isNormal, response = await getResponse(groupId, MessageSettings, user)
        if not isNormal:
            return response
        chetn = user.getChetn()
        today = datetime.date.today() + datetime.timedelta(days=tomorrow)

        if len(response) < 2 and user.role != 6:
            return "\n&#10060;\tРасписание еще не доступно.&#10060;"
        elif user.role == 6 and len(response) < 2:
            return "\n&#10060;Сначала необходимо загрузить расписание. Сделать это можно через меню старосты. Ознакомьтесь с инструкцией"
        try:
            response = response[str(datetime.date(today.year, today.month, today.day).isoweekday())]
            result = ''
            now = datetime.datetime.now() + datetime.timedelta(days=tomorrow)
            month = now.month
            if month < 10:
                month = "0" + str(month)
            day = str(now.day) + "." + str(month)
            for elem in response:
                dateinstr = (str((elem["dayDate"]).rstrip())).find(day)

                try:
                    isPotok = True if elem["potok"] == '1' else False
                except:
                    print('Ошибка:\n', traceback.format_exc())
                    isPotok = False
                if isPotok:
                    if not user_potok:
                        continue

                if '---' in (elem["audNum"]).rstrip():
                    elem["audNum"] = "-нет-"
                if '---' in (elem["buildNum"]).rstrip():
                    elem["buildNum"] = "-нет-"

                # print(dateinstr)
                if (elem["dayDate"]).rstrip() == "чет" and (
                        (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                    result += str(chr(10148)) + elem["dayDate"][:3] + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                                         "disciplType"][
                                                                                                                     :4] + " " + \
                              elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                                  elem["buildNum"]).rstrip() + ' зд.\n'
                elif (elem["dayDate"]).rstrip() == "неч" and not (
                        (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                    result += str(chr(10148)) + elem["dayDate"][:3] + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                                         "disciplType"][
                                                                                                                     :4] + " " + \
                              elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                                  elem["buildNum"]).rstrip() + ' зд.\n'
                elif (elem["dayDate"]).rstrip() == "неч/чет" and not (
                        (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                    result += str(chr(10148)) + " 1&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                               "disciplType"][
                                                                                                           :4] + " " + elem[
                                  "disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                                  elem["buildNum"]).rstrip() + ' зд.\n'
                elif (elem["dayDate"]).rstrip() == "неч/чет" and (
                        (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                    result += str(chr(10148)) + " 2&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                               "disciplType"][
                                                                                                           :4] + " " + elem[
                                  "disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                                  elem["buildNum"]).rstrip() + ' зд.\n'
                elif (elem["dayDate"]).rstrip() == "чет/неч" and (
                        (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                    result += str(chr(10148)) + " 1&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                               "disciplType"][
                                                                                                           :4] + " " + elem[
                                  "disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                                  elem["buildNum"]).rstrip() + ' зд.\n'
                elif (elem["dayDate"]).rstrip() == "чет/неч" and not (
                        (datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                    result += str(chr(10148)) + " 2&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                               "disciplType"][
                                                                                                           :4] + " " + elem[
                                  "disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                                  elem["buildNum"]).rstrip() + ' зд.\n'
                elif dateinstr != -1:
                    result += str(chr(10148)) + str(day) + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem[
                                                                                                              "disciplType"][
                                                                                                          :4] + " " + elem[
                                  "disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (
                                  elem["buildNum"]).rstrip() + ' зд.\n'
                elif not ((elem["dayDate"]).rstrip() == "чет") and not ((elem["dayDate"]).rstrip() == "неч"):
                    result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + \
                              elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (
                                  elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
            return result
        except:
            print('Ошибка:\n', traceback.format_exc())
    except ConnectionError as err:
        return "&#9888;Ошибка подключения к серверу типа ConnectionError. Вероятно, сервера КАИ были выведены из строя.&#9888;"
    except aiohttp.ServerTimeoutError as err:
        return "&#9888;Ошибка подключения к серверу типа Timeout. Вероятно, сервера КАИ перегружены.&#9888;"
    except KeyError as err:
        return False
    except:
        print('Ошибка:\n', traceback.format_exc())

        return ""
    user_potok = user.potokLecture


async def getResponse(groupId,MessageSettings, user):
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
                                              headers={'Content-Type': "application/x-www-form-urlencoded", "user-agent": "BOT RASPISANIE v.1"},
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
        except aiohttp.ServerTimeoutError as err:
            return False, "&#9888;Ошибка подключения к серверу типа Timeout. Вероятно, сервера КАИ перегружены.&#9888;"
        except:
            print('Ошибка:\n', traceback.format_exc())
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
                assert json.dumps(response), "Расписание имеет некорректную форму"
                sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(
                    json.dumps(response), datetime.date.today(), groupId)
                cursor.execute(sql)
                connection.commit()
                return True, response
            except:
                print('Ошибка:\n', traceback.format_exc())
                return True, json.loads(timetable)
        else:
            result = timetable
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
                    sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(
                        json.dumps(response), datetime.date.today(), groupId)
                    cursor.execute(sql)
                    connection.commit()
                    return True, response
                except:
                    print('Ошибка:\n', traceback.format_exc())
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
        print('Ошибка:\n', traceback.format_exc())
        return False, "\n&#9888; Вы выбрали отображать собственное расписание, загруженное из Excele таблицы. В базе отсутствует такое расписание. Чтобы это исправить - либо загрузите расписание, либо смените в профиле способ получения расписания на 'Использовать расписание группы' &#9888;\n"


command = command_class.Command()

command.keys = ['на сегодня', 'расписание на сегодня', 'сегодня']
command.desciption = 'Расписание на сегодня (с учетом четности)'
command.process = info
command.payload = "today"
command.role = [1, 3, 6]
