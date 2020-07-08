import command_class
import vk_api
import random
import datetime
import json
import requests
import keyboards
from main import vk
from message_class import MessageSettings
from user_class import UserParams

today = datetime.date.today()
chetn = UserParams.getChetn()
BASE_URL = 'https://kai.ru/raspisanie'
BASE_URL_STAFF = "https://kai.ru/for-staff/raspisanie"

def info():
    id = MessageSettings.getId()
    group = UserParams.getGroup()
    vk.method("messages.send",
                        {"peer_id": id, "message": showAllTimetable(group, UserParams.login), "keyboard": keyboards.getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})
    return "ok"

def showAllTimetable(groupId, login):
    response = requests.post( BASE_URL_STAFF, data = "prepodLogin=" + str(login), headers = {'Content-Type': "application/x-www-form-urlencoded"}, params = {"p_p_id":"pubLecturerSchedule_WAR_publicLecturerSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"} )
    print("TEST")
    print("Response: ", response.status_code)
    if str(response.status_code) != '200':
        return "&#9888; Возникла ошибка при подключении к серверам. \nКод ошибки: " + str(response.status_code) + " &#9888;"
    response = response.json()
    if len(response) == 0:
        return "\n&#10060;\tРасписание еще не доступно.&#10060;"
    result = ''
    res = ''
    try:
        result += "&#128204;Понедельник&#128204;\n"
        day = response[str(1)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Вторник&#128204;\n"
        day = response[str(2)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Среда&#128204;\n"
        day = response[str(3)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Четверг&#128204;\n"
        day = response[str(4)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Пятница&#128204;\n"
        day = response[str(5)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        result += "\n"
    except Exception as E:
        result += "Нет данных для отображения."
    try:
        result += "&#128204;Суббота&#128204;\n"
        day = response[str(6)]
        for elem in day:
            result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["group"].rstrip() + ' ' + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
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