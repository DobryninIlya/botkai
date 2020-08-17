from .. import classes as command_class
import random
import requests
from ..keyboards import GetButtonTask
from ..classes import vk as vk
from ..classes import MessageSettings
from ..classes import UserParams
import traceback
import datetime
today = datetime.date.today()
chetn = UserParams.getChetn()
BASE_URL = 'https://kai.ru/raspisanie' 

def info():
    today = datetime.date.today()
    date = str(datetime.date(today.year, today.month, today.day)  + datetime.timedelta(days=1))
    group = UserParams.getGroup()
    id = MessageSettings.getId()

    try:
        Timetable =  showTimetable(group, 0)
        if Timetable:
            vk.method("messages.send",
                        {"peer_id": id, "message": "Расписание экзаменов:\n" + Timetable, "random_id": random.randint(1, 2147483647)})
        else:
            vk.method("messages.send",
                        {"peer_id": id, "message": "Расписание экзаменов недоступно.", "keyboard": GetButtonTask(date), "random_id": random.randint(1, 2147483647)})
                        
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        vk.method("messages.send",
                    {"peer_id": id, "message": "Расписание экзаменов недоступно.", "keyboard": GetButtonTask(date), "random_id": random.randint(1, 2147483647)})

    return "ok"

def showTimetable(groupId, tomorrow=0):
    try:
        chetn = UserParams.getChetn()
        today = datetime.date.today() + datetime.timedelta(days=tomorrow)
        response = requests.post( BASE_URL, data = "groupId=" + str(groupId), headers = {'Content-Type': "application/x-www-form-urlencoded"}, params = {"p_p_id":"pubStudentSchedule_WAR_publicStudentSchedule10","p_p_lifecycle":"2","p_p_resource_id":"examSchedule"} )
        print("TEST")
        print("Response: ", response.status_code)
        if str(response.status_code) != '200':
            return "&#9888; Возникла ошибка при подключении к серверам. \nКод ошибки: " + str(response.status_code) + " &#9888;"
        response = response.json()
        if len(response) == 0:
            return "\n&#10060;\tНет элементов для отображения.&#10060;"
        
        result = ''
        for elem in response:
            result += str(chr(10148)) + (elem["examDate"]).lstrip().rstrip() + " " + (elem["examTime"]).lstrip().rstrip() + " " + (elem["disciplName"]).lstrip().rstrip() + " " + (elem["audNum"]).lstrip().rstrip() + " ауд. " + (elem["buildNum"]).lstrip().rstrip() + " зд. \n"
        return result
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
command = command_class.Command()

command.keys = ['экзамены', 'расписание экзаменов', 'exams']
command.desciption = 'Расписание экзаменов'
command.process = info
command.payload = "exams"
command.role = [1,3]