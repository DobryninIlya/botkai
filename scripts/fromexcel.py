import openpyxl

from pprint import pprint
# from ..botkai.classes import vk, cursor, connection
import psycopg2
import vk_api
import json
import os
import sqlite3
import time
print(os.getcwd())


class connections:
    def __init__(self):
        self.connection = psycopg2.connect(dbname=os.getenv('DB_NAME'), user= os.getenv('DB_USER'), password= os.getenv('DB_PASSWORD'), host= os.getenv('DB_HOST'))
        self.connection.autocommit=True
        self.cursor = self.connection.cursor()
        self.conn = sqlite3.connect("bot.db")
        self.cursorR = self.conn.cursor()

connect = connections()
cursor = connect.cursor
cursorR = connect.cursorR
connection = connect.connection
conn = connect.conn

class vk_interface:
    def __init__(self):
        self.token = os.getenv("VK_TOKEN")
        self.vk = vk_api.VkApi(token=self.token)
        self.secret_key = os.getenv("SECRET_KEY")
        self.vk_widget_token = vk_api.VkApi(token=os.getenv("VK_TOKEN_WIDGET"))

vk_interface_obj = vk_interface()
vk = vk_interface_obj.vk
vk_widget = vk_interface_obj.vk_widget_token
secret_key = vk_interface_obj.secret_key



wb = openpyxl.load_workbook(filename = 'scripts//shed.xlsx')
# sheet = wb['"Лист1"']
sheet = wb[wb.sheetnames[0]]
# vals = [v[0].value for v in sheet.range('A1:A2')]
# vals = [v.value for v in sheet]
# group = {}
# group_name_prev = '4131'

weekdays = {
    "пн" : 1,
    "вт" : 2,
    "ср" : 3,
    "чт" : 4,
    "пт" : 5,
    "сб" : 6,
	'none': 0,


}
# first = True
# for row in sheet.rows:
#     if first:
#         first = False
#         continue
#     string = ''
#     # for cell in row:
#         # if str(row[0].value) == '4438':
#             # string = string + str(cell.value) + ' '
#     group_name = str(row[0].value)
#     if True:
#         group[group_name] = {
#             weekdays[(str(row[1].value)).rstrip()] : [
#                 {
#                     "dayDate" : row[3].value, # чет неч
#                     "dayTime" : row[2].value, # время
#                     "disciplType" : row[5].value, # пр лек лр
#                     "disciplName" : row[4].value, # название пары
#                     "audNum" : row[6].value,# аудитория
#                     "buildNum" : row[7].value,# здание
#                     "prepodName" : row[9].value,# здание
#                 }] if not weekdays[(str(row[1].value)).rstrip()] else weekdays[(str(row[1].value)).rstrip()].append(
#                     {
#                     "dayDate" : row[3].value, # чет неч
#                     "dayTime" : row[2].value, # время
#                     "disciplType" : row[5].value, # пр лек лр
#                     "disciplName" : row[4].value, # название пары
#                     "audNum" : row[6].value,# аудитория
#                     "buildNum" : row[7].value,# здание
#                     "prepodName" : row[9].value,# здание
#                     }
#                 )
            
#         }

#     pprint(group['4441'])


    # group_name_prev = group_name




import requests
import json
import traceback

BASE_URL = 'https://kai.ru/raspisanie'


def getGroupsResponse(groupNumber):
    try:
        cursor.execute("SELECT shedule FROM saved_timetable WHERE groupp = 1")
        result = cursor.fetchone()[0]
        result = json.loads(result)
        for elem in result:
            if int(elem["group"]) == int(groupNumber):

                return elem["id"]
        return False
    except:
        print('Ошибка GET GROUP RESPONSE:\n', traceback.format_exc())
        return False




def showGroupId(groupNumber):
    # id = int(MessageSettings.id)
    try:
        response = requests.post(
            BASE_URL,
            headers={'Content-Type': "application/x-www-form-urlencoded"}, timeout=8)
        response = requests.post( BASE_URL + "?p_p_id=pubStudentSchedule_WAR_publicStudentSchedule10&p_p_lifecycle=2&p_p_resource_id=getGroupsURL&query=" + groupNumber,
                                  headers = {'Content-Type': "application/x-www-form-urlencoded"},
                                  params = {"p_p_id":"pubStudentSchedule_WAR_publicStudentSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"}, timeout=8)

        print(response.status_code, response)
        if str(response.status_code) != '200':
            raise ConnectionError
            # vk.method("messages.send",
            #     {"peer_id": id, "message": "&#9888;Ошибка подключения к серверам.&#9888; \n Вероятно, на стороне kai.ru произошел сбой. Вам необходимо продолжить регистрацию как только сайт kai.ru станет доступным.", "random_id": random.randint(1, 2147483647)})
            # vk.method("messages.send",
            #         {"peer_id": id, "message": "test" , "sticker_id" : 18486 , "random_id": random.randint(1, 2147483647)})
            
            return False
        response = response.json()[0]
        return response['id']
    except IndexError:
        # vk.method("messages.send",
        #         {"peer_id": id, "message": "Такой группы нет.", "random_id": random.randint(1, 2147483647)})
        return False
    except (ConnectionError, TimeoutError, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        try:
            group = getGroupsResponse(groupNumber)
            if group:
                return group
            # vk.method("messages.send",
            #         {"peer_id": id, "message": "&#9888;Ошибка подключения к серверам.&#9888; \n Вероятно, на стороне kai.ru произошел сбой. Вам необходимо продолжить регистрацию (ввод номера группы) как только сайт kai.ru станет доступным.", "random_id": random.randint(1, 2147483647)})
            # vk.method("messages.send",
            #         {"peer_id": id, "message": "test" , "sticker_id" : 18486 , "random_id": random.randint(1, 2147483647)})
            return False
        except:
            print('Ошибка:\n', traceback.format_exc())
        return False
    except:
        group = getGroupsResponse(groupNumber)
        if group:
            return group
        print('Ошибка:\n', traceback.format_exc())
        return False



import sqlite3
import psycopg2


try:
    cursorR.execute("""CREATE TABLE saved_timetable(
        id int4 PRIMARY KEY,
        groupp varchar(10),
        daynum varchar(10),
        daydate varchar(10),
        daytime varchar(10),
        disipltype varchar(10),
        disciplname varchar(100),
        audnum varchar(10),
        buildnum varchar(10),
        prepodname varchar(100)
        )""")
except:
    cursorR.execute("DROP TABLE saved_timetable")
    cursorR.execute("""CREATE TABLE saved_timetable(
        id int4 PRIMARY KEY,
        groupp varchar(10),
        daynum varchar(10),
        daydate varchar(10),
        daytime varchar(10),
        disipltype varchar(10),
        disciplname varchar(100),
        audnum varchar(10),
        buildnum varchar(10),
        prepodname varchar(100)
        )""")
conn.commit()
first = True # change true
i = 0
for row in sheet.rows:
    if first:
        first = False
        continue
    string = ''
    for item in row:
        print(str(item.value) + " | ")
    sql = "INSERT INTO saved_timetable VALUES ({id},'{groupp}', '{daynum}', '{daydate}', '{daytime}', '{discipltype}', '{disciplname}', '{audnum}', '{buildnum}', '{prepodname}')".format(
        id = i,
        groupp = str(row[0].value), # чет неч
        daynum = weekdays[str(row[1].value).rstrip().lower()], # чет неч
        daydate = str(row[3].value), # чет неч
        daytime = row[2].value, # время
        discipltype = row[5].value, # пр лек лр
        disciplname  = row[4].value, # название пары
        audnum = row[6].value,# аудитория
        buildnum = row[7].value,# здание
        prepodname = row[9].value# здание
    )
    print(sql)
    i += 1
    cursorR.execute(sql)
conn.commit()
cursorR.execute("SELECT DISTINCT groupp FROM saved_timetable")

groups = cursorR.fetchall()

shed = {}
for group in groups:
    group = group[0]
    # if int(group) < 2214:
    #     continue
    sql = "SELECT * FROM saved_timetable WHERE groupp = {group} ORDER BY daynum, daytime".format(group = group)
    print(sql)
    try:
        cursorR.execute(sql)
    except:
        continue
    result = cursorR.fetchall()
    # pprint(cursor.fetchall())
    week_shed = {}
    prev_day = 1
    shed_day = []
    for row in result:
        day = int(row[2])
        if prev_day == day:
            shed_day.append(
                {
                "dayDate" : row[3], # чет неч
                "dayTime" : row[4], # время
                "disciplType" : row[5], # пр лек лр
                "disciplName" : row[6], # название пары
                "audNum" : row[7],# аудитория
                "buildNum" : row[8],# здание
                "prepodName" : row[9],# здание
                }
            )
        else:
            week_shed[prev_day] = shed_day
            shed_day = [
                {
                "dayDate" : row[3], # чет неч
                "dayTime" : row[4], # время
                "disciplType" : row[5], # пр лек лр
                "disciplName" : row[6], # название пары
                "audNum" : row[7],# аудитория
                "buildNum" : row[8],# здание
                "prepodName" : row[9],# здание
                }
            ]
        prev_day = day
    week_shed[day] = shed_day
    # time.sleep(60)
    # try:
    #     GroupId = showGroupId(str(group))
    #     sql = "SELECT date_update FROM saved_timetable WHERE groupp = {}".format(GroupId)
    #     cursor.execute(sql)
    #     res = cursor.fetchone()[0]
    #     print(res, " DATE_UPDATE--------------------")
    #     if res == '2022-08-26':
    #         continue
    #     connection.commit()
    # except:
    #     pass
    try:
        GroupId = showGroupId(str(group))
        if not GroupId:
            print("SKIP ============ ", group, GroupId)
            continue
        # while not GroupId:
        #     print("=============================\n",
        #           "Для продолжения перезагрузи VPN и нажми клавишу",
        #           "\n=============================\n")
        #     input()
        #     GroupId = showGroupId(str(group))
        sql = "INSERT INTO saved_timetable VALUES ({}, '{}', '{}')".format(GroupId, '2022-08-29', (json.dumps(week_shed)).replace('None', ""))
        cursor.execute(sql)
        connection.commit()
    except:

        sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format((json.dumps(week_shed)).replace('None', ""), '2022-08-29', GroupId)
        cursor.execute(sql)
        # connection.commit()
    connection.commit()
        

cursorR.execute("SELECT * FROM saved_timetable WHERE groupp = '4115' AND daynum = '6'")
pprint(cursorR.fetchall())
