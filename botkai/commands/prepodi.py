from .. import classes as command_class
import random
import datetime
import json
import requests
from ..keyboards import getMainKeyboard
from ..classes import vk as vk
from ..classes import MessageSettings
from ..classes import UserParams
import traceback


chetn = UserParams.getChetn()
BASE_URL = 'https://kai.ru/raspisanie' 
prepodList = []

def info():


    group = UserParams.getGroup()
    id = MessageSettings.getId()
    #vk.method("messages.send",
    #        {"peer_id": id, "message": GetPrepodList() , "keyboard": getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})

    prepodList = GetPrepodList()
    try:
        
        vk.method("messages.send",
            {"peer_id": id, "message": prepodList, "keyboard": getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})
    except:
        st = "&#128104;&#8205;&#127979;"
        pos = prepodList[2400:].rfind(st)
        vk.method("messages.send",
            {"peer_id": id, "message": prepodList[:pos], "keyboard": getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})
        vk.method("messages.send",
            {"peer_id": id, "message": prepodList[pos:], "keyboard": getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})
            
            

            


    #if len(prepodList) > 2400:
    #    vk.method("messages.send",
    #        {"peer_id": id, "message": prepodList[:3000] , "keyboard": getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})
    #    vk.method("messages.send",
    #        {"peer_id": id, "message": prepodList[3000:] , "keyboard": getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})
    #else:
    #    vk.method("messages.send",
    #        {"peer_id": id, "message": prepodList, "keyboard": getMainKeyboard(UserParams.role), "random_id": random.randint(1, 2147483647)})

    return "ok"


class Prepodi:
    def __init__(self):
       self.disciplType = ""
       self.disciplName = ""
       self.prepodName = ""





def getResponse(groupId):
    
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
                raise Exception
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

def GetPrepodList():
    prepodList.clear()
    groupId = UserParams.getGroup()
    isNormal, response = getResponse(groupId)
    if not isNormal:
            return response
    #print("TEST")
    #print("Response: ", response.status_code)
    if str(response.status_code) != '200':
        return "&#9888; Возникла ошибка при подключении к серверам. \nКод ошибки: " + str(response.status_code) + " &#9888;"
    response = response.json()
    if len(response) == 0:
        return "\n&#10060;\tРасписание еще не доступно.&#10060;"
    result = ''
    for key in response:
        for elem in response[key]:
            Prepod = Prepodi()
            Prepod.disciplName = elem["disciplName"]
            Prepod.disciplType = elem["disciplType"]
            Prepod.prepodName = elem["prepodName"]
            if elem["prepodName"].rstrip() == "":
                Prepod.prepodName = ":не-задан:"
            prepodList.append(Prepod)
    prepodList.sort(key=lambda Prepodi: Prepodi.disciplName)
    i = 0
    for prepod in prepodList:
        disciplType = []
        disciplType.append(prepod.disciplType)
        try:
            while prepod.prepodName == prepodList[i+1].prepodName:
                disciplType.append(prepodList[i+1].disciplType)
                prepodList.pop(i)
        except:
            pass  
        i+=1
        if disciplType:
            st = ""
            for discipl in disciplType:
                st += str(discipl).rstrip() + ", "
            st = st[:-2]
            print(prepod.disciplName, st)
            prepod.disciplType = st

    for prepod in prepodList:
        print(prepod.prepodName, prepod.disciplType)
    resultList = []
    for elem in prepodList:
        
        res = "&#128104;&#8205;&#127979;[" + str(elem.disciplType) + "] " + (str(elem.disciplName)).rstrip() + " \n" + ((str(elem.prepodName)).rstrip()).title()
        if res not in resultList:
            resultList.append(res)
    for row in resultList:
        result += "\n---------------------------------------------------\n" + row
    del Prepod
    return result[len("----------------------------------------------------"):]
            



command = command_class.Command()

command.keys = ['преподы', 'преподаватели', '!преподы', 'учителя']
command.desciption = 'список преподавателей и дисциплин'
command.process = info
command.payload = "prepod"