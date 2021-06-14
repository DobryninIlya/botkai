import datetime
import json
import random
import sqlite3
import traceback

import openpyxl
import psycopg2
import requests

from .. import classes as command_class
from ..classes import vk, MessageSettings, UserParams
from ..keyboards import KeyboardProfile

weekdays = {
    "пн": 1,
    "вт": 2,
    "ср": 3,
    "чт": 4,
    "пт": 5,
    "сб": 6,

}




BASE_URL = 'https://kai.ru/raspisanie'


conn = sqlite3.connect("bot.db")
cursorR = conn.cursor()

connection = psycopg2.connect(dbname='dfdn09mdk3r1gr', user='olkywigpsefwye',
                              password='6f73707c0610067f60ed525f472fcbc34e3af291dbc21e6bec1d6d3ed89c94b9',
                              host='ec2-54-246-121-32.eu-west-1.compute.amazonaws.com')
connection.autocommit = True
cursor = connection.cursor()

def ClearDatabase():
    try:
        cursorR.execute("""CREATE TABLE saved_timetable(
            id int4 PRIMARY KEY,
            daynum varchar(10),
            daydate varchar(10),
            daytime varchar(10),
            disipltype varchar(10),
            disciplname varchar(100),
            audnum varchar(10),
            buildnum varchar(10),
            potok varchar(1),
            prepodname varchar(100)
            )""")
    except:
        cursorR.execute("DROP TABLE saved_timetable")
        cursorR.execute("""CREATE TABLE saved_timetable(
            id int4 PRIMARY KEY,
            daynum varchar(10),
            daydate varchar(10),
            daytime varchar(10),
            disipltype varchar(10),
            disciplname varchar(100),
            audnum varchar(10),
            buildnum varchar(10),
            potok varchar(1),
            prepodname varchar(100)
            )""")
    conn.commit()

def isValid(row):
    # День недели
    if str(row[0].value).lower().rstrip() not in ['пн', 'вт', 'ср', "чт", 'пт', 'сб']:
        return False, "День недели указан неправильно. Значения должны быть из следующего списка:'пн', 'вт', 'ср', 'чт', 'пт', 'сб'"
    # Время
    elif str(row[1].value)[:5] not in ['08:00', '09:40', '11:20', '12:50', '13:30', '15:10', '16:40', '18:20']:
        return False, "Время указано неверно. Значения должны быть из следующего списка: '8:00', '9:40', '11:20', '12:50', '13:30', '15:10', '16:40', '18:20'"
    # Частота повторений
    elif len(str(row[2].value)) > 10:
        return False, "Значение частоты повторений пары слишком длинное. Максимум 10 символов"
    # Название
    elif len(str(row[3].value))> 100:
        return False, "Значение длины пары слишком длинное. Максимум 100 символов"
    # Тип пары
    elif len(str(row[4].value))> 10:
        return False, "Значение типа пары слишком длинное. Максимум 10 символов"
    # Аудитория
    elif len(str(row[5].value)) > 20:
        return False, "Значение аудитории слишком длинное. Максимум 20 символов"
    # Здание
    elif str(row[6].value).rstrip() not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        return False, "Значение здания неправильно. Должно быть от 1 до 8"
    # Препод
    elif len(str(row[7].value)) > 100:
        return False, "Значение длины имени преподавателя слишком длинное."
    else:
        return True, ""


def info():
    try:
        id = MessageSettings.getId()
        ClearDatabase()
        url,name = MessageSettings.getAttUrl()

        if not len(url):
            vk.method("messages.send",
                      {"peer_id": id,
                       "message": "Ошибка. Вы не прикрепили файл.",
                       "random_id": random.randint(1, 2147483647)})
            return

        file = open("shed.xlsx", "wb")
        ufr = requests.get(url)
        file.write(ufr.content)
        file.close()


        wb = openpyxl.load_workbook(filename='shed.xlsx')
        try:
            sheet = wb['Лист1']
        except:
            vk.method("messages.send",
                      {"peer_id": id,
                       "message": "Ошибка заполенния файла. Имя листа книги не 'Лист1'", "random_id": random.randint(1, 2147483647)})
            return

        global weekdays, conn, cursorR
        first = True
        i = 0
        for row in sheet.rows:
            if row[0].value == None:
                break
            if first:
                first = False
                continue
            string = ''
            isTrue, msg = isValid(row)
            if not isTrue:
                vk.method("messages.send",
                          {"peer_id": id,
                           "message": "Ошибка чтения расписания. Строка: {}\n".format(i+2)+ msg + "\nЗагрузка файла отменена",
                           "random_id": random.randint(1, 2147483647)})
                return
            sql = "INSERT INTO saved_timetable VALUES ({id}, '{daynum}', '{daydate}', '{daytime}', '{discipltype}', '{disciplname}', '{audnum}', '{buildnum}','{potok}', '{prepodname}')".format(
                id=i,
                daynum=weekdays[str(row[0].value).rstrip().lower()],  # день недели
                daydate=str(row[2].value),  # время
                daytime=row[1].value,  # частота повторений
                discipltype=row[4].value,  # тип пары
                disciplname=row[3].value,  # название пары
                audnum=row[5].value,  # аудитория
                buildnum=str(row[6].value).rstrip(),  # здание
                potok = 1 if row[7].value else 0, # поток или не поток
                prepodname=row[8].value,  # имя препода
            )
            i += 1
            cursorR.execute(sql)

            conn.commit()

        if i < 2:
            vk.method("messages.send",
                      {"peer_id": id,
                       "message": "Ошибка чтения расписания. Файл пуст.",
                       "random_id": random.randint(1, 2147483647)})
            return

        sql = "SELECT * FROM saved_timetable ORDER BY daynum, daytime"
        cursorR.execute(sql)
        result = cursorR.fetchall()
        week_shed = {}
        prev_day = 1
        shed_day = []
        day = ""
        for row in result:

            day = int(row[1])
            if prev_day == day:
                shed_day.append(
                    {
                        "dayDate": row[2],  # чет неч
                        "dayTime": row[3],  # время
                        "disciplType": row[4],  # пр лек лр
                        "disciplName": row[5],  # название пары
                        "audNum": row[6],  # аудитория
                        "buildNum": row[7],  # здание
                        "prepodName": row[9],  # здание
                        "potok": row[8]
                    }
                )


            else:
                week_shed[prev_day] = shed_day
                shed_day = [
                    {
                        "dayDate": row[2],  # чет неч
                        "dayTime": row[3],  # время
                        "disciplType": row[4],  # пр лек лр
                        "disciplName": row[5],  # название пары
                        "audNum": row[6],  # аудитория
                        "buildNum": row[7],  # здание
                        "prepodName": row[9],  # здание
                        "potok": row[8]
                    }
                ]
            prev_day = day
        week_shed[day] = shed_day
        if len(week_shed.keys())==0:
            vk.method("messages.send",
                      {"peer_id": id,
                       "message": "Ошибка. Расписание не найдено...",
                       "random_id": random.randint(1, 2147483647)})
        group = 999999999
        print("MessageSettings.command_key : ", MessageSettings.command_key)
        if MessageSettings.command_key == "загрузить расписание староста":
            if UserParams.adminLevel < 2:
                vk.method("messages.send",
                          {"peer_id": id,
                           "message": "Ошибка. Вы не являетесь старостой\nВы можете добавить свое расписание командой 'загрузить расписание'", "keyboard": KeyboardProfile(),
                           "random_id": random.randint(1, 2147483647)})
                return
            group = UserParams.groupId
        else:
            group = 1000000000 + int(id)
            if UserParams.role == 6:
                group = UserParams.groupId
        date = ""
        if datetime.date.today().month > 7:
            date = "{}-12-30".format(datetime.date.today().year)
        else:
            date = "{}-6-30".format(datetime.date.today().year)
        try:

            sql = "INSERT INTO saved_timetable VALUES ({}, '{}', '{}')".format(group, date,
                                                                               (json.dumps(week_shed)).replace('None', ""))
            cursor.execute(sql)
            connection.commit()
            vk.method("messages.send",
                      {"peer_id": id,
                       "message": "Расписание успешно загружено.", "keyboard": KeyboardProfile(),
                       "random_id": random.randint(1, 2147483647)})

        except:
            print("UPDATING SHED")
            sql = "UPDATE saved_timetable SET shedule = '{}', date_update = '{}' WHERE groupp = {}".format(
                (json.dumps(week_shed)).replace('None', ""), date, group)

            cursor.execute(sql)
            connection.commit()
            vk.method("messages.send",
                      {"peer_id": id,
                       "message": "Расписание успешно обновлено.", "keyboard": KeyboardProfile(),
                       "random_id": random.randint(1, 2147483647)})

        if group < 1000000000:
            cursor.execute("SELECT * FROM users WHERE groupp = {}".format(group))
            res = cursor.fetchall()
            users = ""
            for item in res:
                users += str(item[0]) + ","
            users = users[:-1]

            vk.method("messages.send",
                      {"user_ids": users,
                       "message": "Оповещение! Староста изменил расписание группы. Теперь расписание берется из Excel-файла до наступления {}".format(date),
                       "random_id": random.randint(1, 2147483647)})
    except:
        print('Ошибка:\n', traceback.format_exc())


command = command_class.Command()




command.keys = ['загрузить расписание', 'загрузить расписание староста']
command.desciption = 'загрузить свое расписание'
command.process = info
command.payload = "own_shed_upload"


