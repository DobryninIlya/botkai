import datetime
import json
import random
import traceback

import requests
from ics import Calendar, Event

from .. import classes as command_class
from ..classes import vk, MessageSettings, UserParams, cursor, connection
from ..keyboards import submenu

today = datetime.date.today()
chetn = UserParams.getChetn()
BASE_URL = 'https://kai.ru/raspisanie'
tt_dict = {
    "08:00": "05:00",
    "09:40": "06:40",
    "11:20": "08:20",
    "13:30": "10:30",
    "15:10": "12:10",
    "16:50": "13:50",
    "18:25": "15:25",
    "20:00": "17:00",
    "08:00:00": "05:00:00",
    "09:40:00": "06:40:00",
    "11:20:00": "08:20:00",
    "13:30:00": "10:30:00",
    "15:10:00": "12:10:00",
    "16:50:00": "13:50:00",
    "18:25:00": "15:25:00",
    "20:00:00": "17:00:00",
}
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


def makeFile(week, group):
    c = Calendar()
    today = datetime.date.today()
    chetn = UserParams.getChetn()
    current_date = today - datetime.timedelta(days=today.isoweekday()) + datetime.timedelta(days=1)
    isNormal, response = getResponse(group)
    days_in_week = list(response.keys())
    days_in_week.sort()

    current_week = 4
    while (current_week <= week):
        for key in days_in_week:
            if (current_date.month == 12 and current_date.day == 30) or (current_date.month == 7 and current_date.day == 1):
                break
            chetnost = True if (datetime.date(current_date.year, current_date.month, current_date.day).isocalendar()[
                                    1] + chetn) % 2 else False  # Если True чет, False - неч

            print("DATE ", current_date, current_week, "CHETNOST ", chetnost,
                  datetime.date(current_date.year, current_date.month, current_date.day).isocalendar()[
                      1] + chetn)
            for row in response[key]:
                dayDate = row["dayDate"].rstrip().lower()
                prefix = ""

                if (dayDate == 'чет' and not chetnost) or (dayDate == 'неч' and chetnost):
                    continue
                elif dayDate == 'чет/неч':
                    if chetnost:
                        prefix = " (1) гр."
                    else:
                        prefix = " (2) гр."
                elif dayDate == 'неч/чет':
                    if chetnost:
                        prefix = " (2) гр."
                    else:
                        prefix = " (1) гр."

                e = Event()
                tt = row["dayTime"].rstrip() if len(row["dayTime"].rstrip()) < 6 else row["dayTime"].rstrip()[:5]
                tt = tt_dict[tt]
                begin_time = str(current_date) + " {}:00".format(tt)
                # end_time = str(current_date) + " {}:00".format(time_dict[row["dayTime"].rstrip()])
                e.name = prefix + row["disciplType"].rstrip().upper() + " " + row["disciplName"].rstrip()
                e.begin = begin_time
                e.duration = datetime.timedelta(minutes=190 if row["disciplType"].rstrip().upper() == 'Л.Р.' else 90)
                e.location = "В {} ауд. {} зд".format(row["audNum"].rstrip(), row["buildNum"].rstrip())
                e.description = "В {} ауд. {} зд".format(row["audNum"].rstrip(), row["buildNum"].rstrip())
                c.events.add(e)

            current_date = current_date + datetime.timedelta(days=1)
            if str(current_date.isoweekday()) not in days_in_week:
                current_date = current_date + datetime.timedelta(days=1)
                continue
        current_week += 1
    with open('{}.ics'.format(group), 'w') as f:
        f.write(str(c))

def GetDocShedule(group, id):
    makeFile(5, group)
    a = vk.method("docs.getMessagesUploadServer", { "type" : "doc", "peer_id": id })
    b = requests.post(a["upload_url"], files= { "file" : open(str(group)+".ics", "rb")}).json()
    c = vk.method("docs.save", {"file" : b["file"]})
    d = "doc"+str(c["doc"]["owner_id"])+"_"+str(c["doc"]["id"])
    return d


def info():
    groupId = UserParams.groupId
    att = ''
    try:
        att = GetDocShedule(UserParams.groupId, MessageSettings.getPeer_id())
    except:
        print('Ошибка:\n', traceback.format_exc())
    vk.method("messages.send",
                    {"peer_id": MessageSettings.getPeer_id(), "message": "Твое персональное расписание в .ical. \nДоступно на ближайший месяц", "keyboard" : submenu, 'attachment' : att,
                        "random_id": random.randint(1, 2147483647)})

info_command = command_class.Command()

info_command.keys = ['скачать в ical']
info_command.desciption = 'скачать расписание в .ical'
info_command.payload = "exportcalendar"
info_command.process = info
info_command.premium = True
