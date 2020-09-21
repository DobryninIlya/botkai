from .. import classes as command_class
import random
import datetime
import json
import requests
from .. import keyboards
from ..classes import vk as vk,cursor, connection
from ..classes import MessageSettings
from ..classes import UserParams
import traceback

today = datetime.date.today()
chetn = UserParams.getChetn()
BASE_URL = 'https://kai.ru/raspisanie' 

def info():
    id = MessageSettings.getId()
    group = UserParams.getGroup()
    vk.method("messages.send",
                        {"peer_id": id, "message": showAllTimetable(group), "keyboard": keyboards.getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})
    return "ok"

def showAllTimetable(groupId):
    isNormal, response = getResponse(groupId)
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
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Вторник&#128204;\n"
        day = response[str(2)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Среда&#128204;\n"
        day = response[str(3)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Четверг&#128204;\n"
        day = response[str(4)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Пятница&#128204;\n"
        day = response[str(5)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Суббота&#128204;\n"
        day = response[str(6)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."

            

    return result

def getResponse(groupId):
    
    sql = "SELECT * FROM saved_timetable WHERE groupp = {}".format(groupId)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        try:
            
            response = requests.post( BASE_URL, data = "groupId=" + str(groupId), headers = {'Content-Type': "application/x-www-form-urlencoded"}, params = {"p_p_id":"pubStudentSchedule_WAR_publicStudentSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"}, timeout = 3)
            sql = "INSERT INTO saved_timetable VALUES ({}, '{}', '{}')".format(groupId, datetime.date.today(), json.dumps(response.json()))
            cursor.execute(sql)
            connection.commit()
            return True, response.json()
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
                response = requests.post( BASE_URL, data = "groupId=" + str(groupId), headers = {'Content-Type': "application/x-www-form-urlencoded"}, params = {"p_p_id":"pubStudentSchedule_WAR_publicStudentSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"}, timeout = 3)
                sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(json.dumps(response.json()), datetime.date.today(), groupId)
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
            return True, json.loads(result)
    
    


    return 

command = command_class.Command()

command.keys = ['полностью', 'расписание полностью', 'полное расписание', 'полностью расписание', 'расписание']
command.desciption = 'Расписание полностью'
command.process = info
command.payload = "all"
command.role = [1, 3, 5]