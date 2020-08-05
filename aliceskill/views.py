from __future__ import unicode_literals
from django.http import HttpResponse
# Импортируем модули для работы с JSON и логами.
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from pprint import pprint
import os
import psycopg2
import sqlite3

import random
import datetime
import json
import requests
import traceback


sessionStorage = {}
commands = ['расписание']



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


@csrf_exempt
def main(request):
# Функция получает тело запроса и возвращает ответ.
    body = json.loads(request.body)
    pprint(body)

    response = {
        "version": body['version'],
        "session": body['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(body,request, response)

    return HttpResponse( json.dumps( response))


def handle_dialog(body, request, response):
    request = body["request"]
    tokens = request["nlu"]["tokens"]
    entities = request["nlu"]["entities"]
    group_values = ""
    day = ""
    for command in commands:
        if command.lower() in tokens:
            print("Command ", command.lower())
            command = command.lower()
            if command == 'расписание':
                for entity in entities:
                    if entity["type"] == "YANDEX.NUMBER" and len(group_values) <= 4:
                        group_values += str(entity["value"])
                    elif entity["type"] == "YANDEX.DATETIME":
                        day = entity["value"]["day"]

                print(group_values)
            if not group_values:
                response["response"]["text"] = "Повтори все тоже самое, но с номером группы"
            #response["response"]["text"] = command + " " + group_values + " день " + str(day)
            response["response"]["text"] = info(group_values, day)

            return
        else:
            response["response"]["text"] = "Я не распознал твою команду. Повтори, пожалуйста, что ты хочешь получить и номер группы."


today = datetime.date.today()
chetn = 1
BASE_URL = 'https://kai.ru/raspisanie' 
frazi = ["Можно сходить в кино 😚", "Можно почитать 😚", "Можно прогуляться в лесу 😚", "Можно распланировать дела на неделю 😚", "Можно заняться спортом, например. 😚", "Можно вспомнить строчки гимна КАИ 😚", "Можно заняться чем то интересным 😚", "Можно встретиться с друзьями 😚"]
def info(group, day):
    try:
        today = datetime.date.today()
        day = int(day) if (str(day)).isdigit() else 0
        date = str(datetime.date(today.year, today.month, today.day)  + datetime.timedelta(days=1))
        return showTimetable(group, day)
    except:
        print('Ошибка:\n', traceback.format_exc())



def showTimetable(groupId, tomorrow=0):
    try:
        isNormal, response = getResponse(groupId)
        print(response)
        if not isNormal:
            print("NOOOOOOOOOOOO")
            return response
        
        today = datetime.date.today() + datetime.timedelta(days=tomorrow)


        if len(response) == 0:
            return "\n&#10060;\tРасписание еще не доступно.&#10060;"
        
        response = response[str(datetime.date(today.year, today.month, today.day).isoweekday())]
        result = ''
        now = datetime.datetime.now() + datetime.timedelta(days=tomorrow)
        month = now.month
        if month < 10:
            month = "0" + str(month)
        day = str(now.day) + "." + str(month)
        for elem in response:
            dateinstr = (str((elem["dayDate"]).rstrip())).find(day)
            print(dateinstr)
            if (elem["dayDate"]).rstrip()=="чет" and ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148)) + elem["dayDate"][:3] + " " + " &#8987;" + elem["dayTime"][:5] +  " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() +' зд.\n'
            elif (elem["dayDate"]).rstrip()=="неч" and  not ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148)) + elem["dayDate"][:3] + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() +' зд.\n'
            elif (elem["dayDate"]).rstrip()=="неч/чет" and  not ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148))  + " 1&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() +' зд.\n'
            elif (elem["dayDate"]).rstrip()=="неч/чет" and  ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148))  + " 2&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() +' зд.\n'
            elif (elem["dayDate"]).rstrip()=="чет/неч" and  ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148))  + " 1&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() +' зд.\n'
            elif (elem["dayDate"]).rstrip()=="чет/неч" and  not ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                result += str(chr(10148))  + " 2&#8419;гр. " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() +' зд.\n'
            elif dateinstr != -1:
                result += str(chr(10148)) + str(day) + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
            elif not ((elem["dayDate"]).rstrip()=="чет") and not ((elem["dayDate"]).rstrip()=="неч"):
                result += str(chr(10148)) + elem["dayDate"].rstrip() + " " + " &#8987;" + elem["dayTime"][:5] + " " + elem["disciplType"][:4] + " " + elem["disciplName"] + " " + (elem["audNum"]).rstrip() + " " + (elem["buildNum"]).rstrip() + ' зд.\n'
        return result
    except ConnectionError as err:
        return "&#9888;Ошибка подключения к серверу типа ConnectionError. Вероятно, сервера КАИ были выведены из строя.&#9888;"
    except requests.exceptions.Timeout as err:
        return "&#9888;Ошибка подключения к серверу типа Timeout. Вероятно, сервера КАИ перегружены.&#9888;"
    except KeyError as err:
        return False
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())

        return ""
    


def getResponse(groupId):
    try:
        sql = "SELECT * FROM saved_timetable WHERE groupp = {}".format(groupId)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None:
            try:
                
                response = requests.post( BASE_URL, data = "groupId=" + str(groupId), headers = {'Content-Type': "application/x-www-form-urlencoded"}, params = {"p_p_id":"pubStudentSchedule_WAR_publicStudentSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"}, timeout = 3)
            except ConnectionError as err:
                return False, "&#9888;Ошибка подключения к серверу типа ConnectionError. Вероятно, сервера КАИ были выведены из строя.&#9888;"
            except requests.exceptions.Timeout as err:
                return False, "&#9888;Ошибка подключения к серверу типа Timeout. Вероятно, сервера КАИ перегружены.&#9888;"
            except:
                print('Ошибка:\n', traceback.format_exc())

                return False, ""
            sql = "INSERT INTO saved_timetable VALUES ({}, '{}', '{}')".format(groupId, datetime.date.today(), json.dumps(response.json()))
            cursor.execute(sql)
            connection.commit()
            return True, response.json()
        else:
            date_update = result[1]
            timetable = result[2]
            if date_update + datetime.timedelta(days=4) >= today:
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
    except:
        print('Ошибка:\n', traceback.format_exc())
