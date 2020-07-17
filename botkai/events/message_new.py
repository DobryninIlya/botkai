from .. import classes
from .. import keyboards


import sqlite3
import datetime
import json
import random 
import requests
import traceback
import os, importlib

cursor = classes.cursor
cursorR = classes.cursorR
conn = classes.conn
connection = classes.connection

cursorR.execute("""CREATE TABLE Status (ID_VK INT NOT NULL PRIMARY KEY, Status SMALLINT NULL); """)
conn.commit()

today = datetime.date.today()
message_params = {}

vk = classes.vk

UserParams = classes.UserParams
command_list = classes.command_list



def load_modules():
   files = os.listdir("/app/botkai/commands")
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
       importlib.import_module("botkai.commands." + m[0:-3])


load_modules()




def message_new(request):
    try:
        global message_params
        message_params = json.loads(request.body)
        classes.MessageSettings.update(message_params)
        if IsRegistred():
            print("Зарегистрирован")
            UserParams.update(int(message_params["object"]["message"]["from_id"]))

            button = ""
            try:
                print("msg payload", message_params["object"]["message"]['payload'])
                payload = message['payload']
                payload = json.loads(payload)
                button = payload["button"]
                # print(button, payload)
                ##MessageSettings.button = button
                ##MessageSettings.payload = payload


            except Exception as E:
                pass


            if button != "":
                for c in command_list:
                    crole = c.role
                    if button == c.payload and c.admlevel<=UserParams.getAdminLevel():
                        #print("role (command, user) :", crole, UserParams.role)
                        #print("first")
                        if UserParams.role in crole:
                            c.process()
                        return "ok"
                    else:
                        pass
            else:
                #for c in command_list:
                #    if body in c.keys:
                #        c.process()
                #        return "ok"
                #    else:
                #        print("no")
                distance = len(message_params["object"]["message"]["text"])
                command = None
                key = ''
                for c in command_list:
                    
                    if UserParams.role in c.role:
                        
                        for k in c.keys:
                            d = damerau_levenshtein_distance((message_params["object"]["message"]["text"]).lower(), k)
                            if d < distance:
                                distance = d
                                command = c
                                key = k
                                #print(c.role, UserParams.role)
                                if distance == 0 and c.admlevel<=UserParams.getAdminLevel() and (UserParams.role in c.role):
                                    c.process()
                                    return "ok"
                if distance < len(message_params["object"]["message"]["text"])*0.4 and c.admlevel<=UserParams.getAdminLevel()  and (UserParams.role in c.role):
                    
                    mesg = 'Я понял ваш запрос как "%s"' % key 
                    vk.method("messages.send",
                            {"peer_id": int(message_params["object"]["message"]["from_id"]), "message": mesg, "random_id": random.randint(1, 2147483647)})
                    command.process()
                    return "ok"

        
    except:  
        print('Ошибка:\n', traceback.format_exc())  
    
    return "ok"



def IsRegistred():
    try:
        body = message_params["object"]["message"]["text"]
        id = int(message_params["object"]["message"]["from_id"])
        if InBase(id):
            #print("Зарегистрироан")
            return True
        else:

            #print("Не зарегистрирован")
            if InBaseR(id):
                vk.method("messages.send",
                            {"peer_id": id, "message": "test" , "sticker_id" : 6864 , "random_id": random.randint(1, 2147483647)})
                vk.method("messages.send", {"peer_id": id, "message": "Похоже, что ты не зарегистриован. Для работы бота необходима регистрация.\nПо любым вопросам введите Справка в чат, чтобы продолжить пользоваться ботом - выполняйте инструкции.\n Мне нужно понимать кто ты. Выбери соответствующую кнопку в меню", "keyboard" : keyboards.roleMenu,
                                    "random_id": random.randint(1, 2147483647)})
                sql = "INSERT INTO Status VALUES (" + str(id) + ", 3);"
                cursorR.execute(sql)
                conn.commit()
                return False
            elif StatusR(id) == 3:
                
                today = datetime.date.today()
                role = 1
                print(body)
                if body == "Преподаватель":
                    role = 2
                    vk.method("messages.send", {"peer_id": id, "message": "Регистрация для преподавателя временно недоступна", 
                                    "random_id": random.randint(1, 2147483647)})
                    return False
                elif body == "Студент":
                    role = 1
                elif body == "Родитель":
                    role = 3
                elif body == "Абитуриент (поступающий)":
                    role = 4
                    vk.method("messages.send", {"peer_id": id, "message": "Регистрация для абитуриента временно недоступна", 
                                    "random_id": random.randint(1, 2147483647)})
                    return False
                elif body == "Справка":
                    msg = """На данном этапе необходимо указать свою роль. 
                    Если вы студент, вам будут доступно свое расписание, список преподавателей. Вас могут видеть одногруппники в списке группы.
                    Если вы родитель, то вам будет доступно расписание и список преподавателей. Ваш аккаунт будет скрыт от вашего ребенка. Вам также будет доступен список других родителей данной группы.
                    Если вы преподаватель, вам будет доступно ваше расписание и рассылка объявлений группе.
                    
                    """
                    vk.method("messages.send", {"peer_id": id, "message": msg, "keyboard" : keyboards.roleMenu, 
                                    "random_id": random.randint(1, 2147483647)})
                    return False
                else:
                    vk.method("messages.send", {"peer_id": id, "message": "Выберите кнопку меню.", "keyboard" : keyboards.roleMenu, 
                                    "random_id": random.randint(1, 2147483647)})
                    return False
                    
                try:
                    sql = "INSERT INTO Users VALUES (" + str(id) + ", '" + "', " + "0 " + ", 1, 1, 0, '" + str(datetime.date(today.year, today.month, today.day)) +"',0 , 0, 0, '2020-01-01', 0, 0," + str(role) + ");"
                    print(sql)
                    cursor.execute(sql)
                    
                except Exception as E:
                    print('Ошибка commit:\n', traceback.format_exc())
                if role == 1 or role == 3:
                    
                    sql = "UPDATE Status SET Status = 1 WHERE ID_VK = " + str(id) + ";"
                    cursorR.execute(sql)
                    conn.commit()
                    vk.method("messages.send", {"peer_id": id, "message": "Введите свое имя в чат", 
                                    "random_id": random.randint(1, 2147483647)})
                elif role == 2:
                    sql = "UPDATE Status SET Status = 4 WHERE ID_VK = " + str(id) + ";"
                    cursorR.execute(sql)
                    conn.commit()
                    vk.method("messages.send", {"peer_id": id, "message": "Введите свой логин (без лишних символов: пробелов, запятых и тп.)", 
                                    "random_id": random.randint(1, 2147483647)})
                elif role == 4:
                    sql = "DELETE FROM Status WHERE ID_VK = " + str(id) + ";"
                    cursorR.execute(sql)
                    sql = "UPDATE Users SET Groupp = 7777 WHERE ID_VK = " + str(id) + ";"
                    cursor.execute(sql)
                    conn.commit()
                    
                    vk.method("messages.send", {"peer_id": id, "message": "Теперь я знаю о тебе достаточно). \n Используй кнопки клавиатуры.", "keyboard" : keyboards.getMainKeyboard(role = 4),
                                    "random_id": random.randint(1, 2147483647)})
                
                return False
            elif StatusR(id) == 1:
                if body.lower() == "справка":
                    vk.method("messages.send", {"peer_id": id, "message": "По вопросам сотрудничества писать на почту mr.woodysimpson@gmail.com \n Чтобы позвать администратора, введите Позвать.", "keyboard" : keyboards.keyboardRef1, 
                                    "random_id": random.randint(1, 2147483647)})
                    sql = "UPDATE Status SET Status = 15 WHERE ID_VK = " + str(id) + ";"
                    cursorR.execute(sql)
                    conn.commit()
                    return False
                elif body.lower() == "продолжить регистрацию":
                    vk.method("messages.send", {"peer_id": id, "message": "Введите свое имя в чат", "keyboard" : "", 
                                    "random_id": random.randint(1, 2147483647)})
                    sql = "UPDATE Status SET Status = 1 WHERE ID_VK = " + str(id) + ";"
                    cursorR.execute(sql)
                    conn.commit()
                    return False
                today = datetime.date.today()
                sql = "UPDATE users SET name = '" + str(body) + "' WHERE ID_VK = " + str(id)
                cursor.execute(sql)
                
                sql = "UPDATE Status SET Status = 2 WHERE ID_VK = " + str(id) + ";"
                cursorR.execute(sql)
                conn.commit()
                vk.method("messages.send", {"peer_id": id, "message": "Очень приятно, " + str(body) + "",
                                    "random_id": random.randint(1, 2147483647)})
                vk.method("messages.send", {"peer_id": id, "message": "Расписание какой группы мне тебе показывать?\n Отправь сообщение с номером твоей группы.",
                                    "random_id": random.randint(1, 2147483647)})
                return False
            elif StatusR(id) == 2:
                try:
                    if showGroupId(body):
                        if int(body) > 1100 and int(body)<10000:
                            sql = "UPDATE Users SET Groupp= " + str(showGroupId(body)) + " ,groupReal = " + str(body)+ " WHERE ID_VK = " + str(id) + ";"
                            cursor.execute(sql)
                            
                            sql = "DELETE FROM Status WHERE ID_VK = " + str(id) + ";"
                            cursorR.execute(sql)
                            conn.commit()
                            UserParams.update(int(message_params["object"]["message"]["from_id"]))
                            vk.method("messages.send", {"peer_id": id, "message": "Твоя группа: " + body + "\n Теперь мне все понятно и ты можешь пользоваться ботом :)\n Настоятельно рекомендую подписаться на оффициальную группу @botraspisanie. Здесь ты сможешь получить много полезной информации.", "keyboard" : keyboards.getMainKeyboard(UserParams.role),
                                                "random_id": random.randint(1, 2147483647)})
                            vk.method("messages.send",
                                    {"peer_id": id, "message": "test" , "sticker_id" : 6880 , "random_id": random.randint(1, 2147483647)})
                            vk.method("messages.send", {"peer_id": id, "random_id": random.randint(1, 2147483647), "attachment": "poll-182372147_348171795"})

                        elif int(body) > 10000:
                            vk.method("messages.send",
                                {"peer_id": id, "message": "Ваше расписание не поддерживается ввиду его отсутствия на сайте КНИТУ-КАИ. Если вы уверены, что расписание существует на сайте, напишите об этом в Обсуждениях @botraspisanie", "random_id": random.randint(1, 2147483647)})
                        else:
                            vk.method("messages.send", {"peer_id": id, "message": "Я не могу обработать такой номер группы. ", 
                                                "random_id": random.randint(1, 2147483647)})
                        return False
                    else:
                        vk.method("messages.send", {"peer_id": id, "message": "Что-что, а это точно не номер группы. Повтори ввод.", 
                                                    "random_id": random.randint(1, 2147483647)})
                                
                except Exception as E:
                    print('Ошибка:\n', traceback.format_exc())
                    return False
            elif StatusR(id) == 4:
                try:

                    body = body.lower()
                    response = requests.post( BASE_URL_STAFF, data = "prepodLogin=" + str(body), headers = {'Content-Type': "application/x-www-form-urlencoded"}, params = {"p_p_id":"pubLecturerSchedule_WAR_publicLecturerSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"} )
                    #print(len(response.json()))
                    if not len(response.json()):
                        vk.method("messages.send", {"peer_id": id, "message": "Расписание для вас отсутствует на сайте. Повторите ввод.", 
                                                    "random_id": random.randint(1, 2147483647)})
                    else:
                        sql = "UPDATE users SET login = '" + body + "' WHERE ID_VK = " + str(id)
                        cursor.execute(sql)
                        
                        sql = "UPDATE users SET role = 2 WHERE ID_VK = " + str(id)
                        cursor.execute(sql)
                        
                        sql = "DELETE FROM Status WHERE ID_VK = " + str(id) + ";"
                        cursorR.execute(sql)
                        conn.commit()
                        UserParams.update()
                        vk.method("messages.send", {"peer_id": id, "message": "Регистрация успешно завершена.", "keyboard": keyboards.getMainKeyboard(UserParams.role),
                                                    "random_id": random.randint(1, 2147483647)})
                        #print(UserParams.login, UserParams.role)
                except Exception as E:
                    print('Ошибка:\n', traceback.format_exc())
                    return False





            elif StatusR(id) == 15:
                try:
                    if body.lower() == "позвать":
                        vk.method("messages.send", {"peer_id": 159773942, "message": "Пользователь @id"+str(id) + " просит помощи" , "keyboard": keyboards.getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})
                        vk.method("messages.send", {"peer_id": id, "message": "Сообщение администратору отправлено", "keyboard": keyboards.keyboardRef1, "random_id": random.randint(1, 2147483647)})
                        return False
                    elif body.lower() == "справка":
                        vk.method("messages.send", {"peer_id": id, "message": "По вопросам сотрудничества писать на почту mr.woodysimpson@gmail.com \n Чтобы позвать администратора, введите Позвать.", "keyboard" : keyboards.keyboardRef, 
                                        "random_id": random.randint(1, 2147483647)})
                        sql = "UPDATE Status SET Status = 15 WHERE ID_VK = " + str(id) + ";"
                        cursor.execute(sql)
                        conn.commit()
                        return False
                    elif body.lower() == "продолжить регистрацию":
                        vk.method("messages.send", {"peer_id": id, "message": "Введите свое имя в чат", "keyboard" : keyboards.keyboardNull, 
                                        "random_id": random.randint(1, 2147483647)})
                        sql = "UPDATE Status SET Status = 1 WHERE ID_VK = " + str(id) + ";"
                        cursorR.execute(sql)
                        conn.commit()
                        return False
                            
                                
                    return False
                except Exception as E:
                    vk.method("messages.send", {"peer_id": id, "message": "Error status 15 in reg", 
                                        "random_id": random.randint(1, 2147483647)})
                return False
    except:  
        print('Ошибка:\n', traceback.format_exc())  



BASE_URL = 'https://kai.ru/raspisanie'
BASE_URL_STAFF = "https://kai.ru/for-staff/raspisanie"
def showGroupId(groupNumber):
    id = int(message_params["object"]["message"]["from_id"])
    try:
        response = requests.post( BASE_URL + "?p_p_id=pubStudentSchedule_WAR_publicStudentSchedule10&p_p_lifecycle=2&p_p_resource_id=getGroupsURL&query=" + groupNumber, headers = {'Content-Type': "application/x-www-form-urlencoded"}, params = {"p_p_id":"pubStudentSchedule_WAR_publicStudentSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"}, timeout = 5 )
        print(response.status_code, response)
        if str(response.status_code) != '200':
            vk.method("messages.send",
                {"peer_id": id, "message": "&#9888;Ошибка подключения к серверам.&#9888; \n Вероятно, на стороне kai.ru произошел сбой. Вам необходимо продолжить регистрацию как только сайт kai.ru станет доступным.", "random_id": random.randint(1, 2147483647)})
            vk.method("messages.send",
                    {"peer_id": id, "message": "test" , "sticker_id" : 18486 , "random_id": random.randint(1, 2147483647)})
            return False
        response = response.json()[0]
        print(response)
        return response['id']
    except IndexError:
        vk.method("messages.send",
                {"peer_id": id, "message": "Такой группы нет.", "random_id": random.randint(1, 2147483647)})
        return False
    except (ConnectionError, TimeoutError, requests.exceptions.Timeout):
        vk.method("messages.send",
                {"peer_id": id, "message": "&#9888;Ошибка подключения к серверам.&#9888; \n Вероятно, на стороне kai.ru произошел сбой. Вам необходимо продолжить регистрацию (ввод номера группы) как только сайт kai.ru станет доступным.", "random_id": random.randint(1, 2147483647)})
        vk.method("messages.send",
                {"peer_id": id, "message": "test" , "sticker_id" : 18486 , "random_id": random.randint(1, 2147483647)})
        return False
    except:
        print('Ошибка:\n', traceback.format_exc())
        return False






def InBaseR(id): ### Проверка на зарегестрированность и наличие в базе Status (RAM)
    sql = "SELECT Status FROM Status WHERE ID_VK=" + str(id) +";"
    cursorR.execute(sql)
    res=cursorR.fetchall()
    if len(res)==0:
        return True
    else:
        return False

def InBase(id): ### Проверка на зарегестрированность и наличие в базе Users
    try:
        #global allCommands, statUser
        #if MessageSettings.statUser.count(id)>1:
        #    MessageSettings.statUser.remove(id)
        #elif MessageSettings.statUser.count(id)==1:
        #    pass;
        #else:
        #    MessageSettings.statUser.append(id)
        #if statUser.count(id) == 0:
        #    statUser.append(id)
        #    MessageSettings.statUser = len(statUser)
        #    print(MessageSettings.statUser)
            
        #allCommands += 1
        #MessageSettings.allCommands = allCommands
        sql = "SELECT Groupp, login, role FROM Users WHERE ID_VK=" + str(id) + ";"
        cursor.execute(sql)
        res=cursor.fetchone()
        if res == None:
            return False
        group = res[0]
        login = ""
        try:
            login = res[1]
        except Exception as E:
            print('Ошибка:\n', traceback.format_exc())
        print("Result: ", res)
        if login:
            print(login)
            return True

        if len(str(group)) == 0:
            print(1)
            return False
        elif int(group) == 0 and int(id)<2000000000:
            print(2)
            return False
        else:
            print(3)
            return True
    except TypeError:
        print('!Ошибка:\n', traceback.format_exc())
        print(4)
        if int(id)>2000000000:
            print(5)
            return True
        print(6)
        return False
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        print("err...............................")
        vk.method("messages.send", {"peer_id": id, "message": "Что-то пошло не так.", 
                                    "random_id": random.randint(1, 2147483647)})
        vk.method("messages.send",
                        {"peer_id": id, "message": "test" , "sticker_id" : 6890 , "random_id": random.randint(1, 2147483647)})
        vk.method("messages.send", {"peer_id": id, "message": "Перезагружаюсь...", 
                                    "random_id": random.randint(1, 2147483647)})
        conn.commit()
        sys.exit(0)
def StatusR(id): ### Текущий статус в таблице Status (RAM)
    sql = "SELECT Status FROM Status WHERE ID_VK=" + str(id)
    cursorR.execute(sql)
    res=cursorR.fetchone()
    if res == None:
        return
    if int(res[0]) > 0:
        return int(res[0])
    else:
        return
    


def damerau_levenshtein_distance(s1, s2):
    d = {}
    lenstr1 = len(s1)
    lenstr2 = len(s2)
    for i in range(-1, lenstr1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, lenstr2 + 1):
        d[(-1, j)] = j + 1
    for i in range(lenstr1):
        for j in range(lenstr2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,  # deletion
                d[(i, j - 1)] + 1,  # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[i - 2, j - 2] + cost)  # transposition
    return d[lenstr1 - 1, lenstr2 - 1]