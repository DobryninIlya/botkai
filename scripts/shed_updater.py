import psycopg2
import vk_api
import sqlite3
import json
import traceback
import os
import requests
import datetime
import time


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

def shed_update():
    sql = "SELECT DISTINCT groupp FROM saved_timetable WHERE groupp > 1000 AND groupp <1000000000"
    cursor.execute(sql)
    result = cursor.fetchall()
    err = 0
    for row in result:
        try:
            groupId = row[0]
            response = requests.post(BASE_URL, data="groupId=" + str(groupId),
                                     headers={'Content-Type': "application/x-www-form-urlencoded"},
                                     params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10",
                                             "p_p_lifecycle": "2", "p_p_resource_id": "schedule"}, timeout=10)
            assert json.dumps(response.json()), "Расписание имеет некорректную форму"
            sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(
                json.dumps(response.json()), datetime.date.today(), groupId)
            if len(json.dumps(response.json())) <5:
                raise Exception
            cursor.execute(sql)
            connection.commit()
        except:
            err += 1
    print("+++++++++++++\nЗавершено. Ошибок: {}/{} \nВремя выполнения: {}\n+++++++++++++".format(err,len(result), time.time() - start_time))
    return
