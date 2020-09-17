import openpyxl

from pprint import pprint

wb = openpyxl.load_workbook(filename = 'shed.xlsx')
sheet = wb['Лист1']

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
        response = requests.post( BASE_URL + "?p_p_id=pubStudentSchedule_WAR_publicStudentSchedule10&p_p_lifecycle=2&p_p_resource_id=getGroupsURL&query=" + groupNumber, headers = {'Content-Type': "application/x-www-form-urlencoded"}, params = {"p_p_id":"pubStudentSchedule_WAR_publicStudentSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"}, timeout = 4)
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
    except (ConnectionError, TimeoutError, requests.exceptions.ReadTimeout):
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
        print('Ошибка:\n', traceback.format_exc())
        return False



import sqlite3
import psycopg2

conn = sqlite3.connect("bot.db")
cursorR = conn.cursor()

connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye', password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9', host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
connection.autocommit=True
cursor = connection.cursor()
# cursorR.execute("DROP TABLE saved_timetable")
# cursorR.execute("""CREATE TABLE saved_timetable(
#     id int4 PRIMARY KEY,
#     groupp varchar(10),
#     daynum varchar(10),
#     daydate varchar(10),
#     daytime varchar(10),
#     disipltype varchar(10),
#     disciplname varchar(100),
#     audnum varchar(10),
#     buildnum varchar(10),
#     prepodname varchar(100)
#     )""")

# conn.commit()
first = True
i = 0
# for row in sheet.rows:
#     if first:
#         first = False
#         continue
#     string = ''

#     sql = """
#     INSERT INTO saved_timetable VALUES({id},'{groupp}', '{daynum}', '{daydate}', '{daytime}', '{discipltype}', '{disciplname}', '{audnum}', '{buildnum}', '{prepodname}')
#     """.format(
#         id = i,
#         groupp = str(row[0].value), # чет неч
#         daynum = weekdays[str(row[1].value).rstrip()], # чет неч
#         daydate = row[3].value, # чет неч
#         daytime = row[2].value, # время
#         discipltype = row[5].value, # пр лек лр
#         disciplname  = row[4].value, # название пары
#         audnum = row[6].value,# аудитория
#         buildnum = row[7].value,# здание
#         prepodname = row[9].value,# здание
#     )
#     i += 1
#     cursor.execute(sql)
# conn.commit()
cursorR.execute("SELECT DISTINCT groupp FROM saved_timetable")

groups = cursorR.fetchall()

shed = {}
for group in groups:
    group = group[0]
    sql = "SELECT * FROM saved_timetable WHERE groupp = {group} ORDER BY daynum, daytime".format(group = group)
    cursorR.execute(sql)
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
    try:
        sql = "INSERT INTO saved_timetable VALUES ({}, '{}', '{}')".format(showGroupId(group), '2020-12-30', json.dumps(week_shed))
        cursor.execute(sql)
        connection.commit()
    except:

        sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(json.dumps(week_shed), '2020-12-30', showGroupId(str(group)))
        cursor.execute(sql)
    connection.commit()
        

# cursorR.execute("SELECT * FROM saved_timetable WHERE groupp = '4438' AND daynum = '6'")
# pprint(cursorR.fetchall())
