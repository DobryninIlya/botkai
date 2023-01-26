import datetime
import json
import os
import sqlite3
import time

import psycopg2
import requests
import traceback

start_time = time.time()
BASE_URL = 'https://kai.ru/raspisanie'

class connections:
    def __init__(self):
        self.connection = psycopg2.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'),
                                           password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'))
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.conn = sqlite3.connect("bot.db")
        self.cursorR = self.conn.cursor()


connect = connections()
cursor = connect.cursor
cursorR = connect.cursorR
connection = connect.connection
conn = connect.conn



shed = ""
date_update = ""
def getGroupsResponse(groupNumber):
    global shed, date_update
    try:
        if not shed:
            cursor.execute("SELECT shedule,date_update FROM saved_timetable WHERE groupp = 1")
            result_query = cursor.fetchone()
            result = result_query[0]
            date_update = result_query[1]
            result = json.loads(result)
            shed = result


        for elem in shed:
            if int(elem["group"]) == int(groupNumber):

                return elem["id"],date_update
        return False, False
    except:
        print('Ошибка GET GROUP RESPONSE:\n', traceback.format_exc())
        return False, False


def showGroupId(groupNumber):
    try:
        group, date_update = getGroupsResponse(groupNumber)
        print(group, date_update)
        if not group:
            return False
        today = datetime.date.today()
        date = datetime.date(today.year, today.month, today.day)
        if date_update == date:
            print("Номер группы взят из кэша, т.к. последнее обновление сегодня, ", date)
            return group
        else:
            response = requests.post(
                BASE_URL + "?p_p_id=pubStudentSchedule_WAR_publicStudentSchedule10&p_p_lifecycle=2&p_p_resource_id=getGroupsURL&query=",
                headers={'Content-Type': "application/x-www-form-urlencoded", "user-agent": "BOT RASPISANIE v.1"},
                params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10", "p_p_lifecycle": "2",
                        "p_p_resource_id": "schedule"}, timeout=8)
            cursor.execute("UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = 1".format(json.dumps(response.json()),date))
            connection.commit()
        group, _ = getGroupsResponse(groupNumber)
        if group:
            return group
        print('Ошибка:\n', traceback.format_exc())
        return False


    except IndexError:
        # vk.method("messages.send",
        #         {"peer_id": id, "message": "Такой группы нет.", "random_id": random.randint(1, 2147483647)})
        return False

    except (ConnectionError, TimeoutError, requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError):
        try:
            group, _ = getGroupsResponse(groupNumber)
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
        group, _ = getGroupsResponse(groupNumber)
        if group:
            return group
        print('Ошибка:\n', traceback.format_exc())
        return False


cursor.execute("SELECT groupReal FROM users WHERE (role = 1 or role = 3) and 'dateChange' > '2022-08-15' and groupReal>0")
# DISTINC в теле запроса не указывать! Мешает группы.
res = cursor.fetchall()
count = len(res)
curr = 0
today = datetime.date.today()
for row in res:
    curr+=1
    groupid = showGroupId(int(row[0]))
    print('CURRENT GROUP IS ', groupid)
    print("UPDATE users SET groupp = {} WHERE groupReal = {}".format(
        groupid, row[0]))
    if not groupid:
        continue
    cursor.execute("UPDATE users SET groupp = {}, \"dateChange\" = '{}' WHERE (role = 1 or role = 3) and groupReal = {}".format(
        groupid, today, row[0]))
    connection.commit()
    print("Обновлено расписание группы ", groupid)
    print(curr, "/", count)
