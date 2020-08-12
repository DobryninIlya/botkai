
import random
import traceback
import json
import datetime
import requests
from .classes import MessageSettings, UserParams, connection, cursor, vk
import os


BASE_URL = 'https://kai.ru/raspisanie'
appid = os.getenv('APP_ID')
city_id = 551487
class UsersDistr:
    def __init__(self):
        self.group = 0
        self.realGroup = 0
        self.users = []
distrList = [] 

def Weather():
    res = ''
    try:
        result = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = result.json()
        res += str(data['weather'][0]['description']) + ", "
        res+= str(data['main']['temp'])

    except Exception as e:
        print("Exception (weather):", e)
        pass
    return res
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

def timetableInfo(groupId, tomorrow=0):
    try:
        chetn = UserParams.getChetn()
        today = datetime.date.today() + datetime.timedelta(days=tomorrow)
        isNormal, response = getResponse(groupId)
        if not isNormal:
            return response
        # print("Response: ", response.status_code)
        # if str(response.status_code) != '200':
        #     return "&#9888; Возникла ошибка при подключении к серверам. \nКод ошибки: " + str(response.status_code) + " &#9888;"
        response = response.json()
        if len(response) == 0:
            return "\n&#10060;\tРасписание еще не доступно.&#10060;"
        response = response[str(datetime.date(today.year, today.month, today.day).isoweekday())]
        result = ''
        now = datetime.datetime.now() + datetime.timedelta(days=tomorrow)
        month = now.month
        if month < 10:
            month = "0" + str(month)
        day = str(now.day) + "." + str(month)
        first = ""
        room = ""
        building = ""

        for elem in response:
            dateinstr = (str((elem["dayDate"]).rstrip())).find(day)
            print(dateinstr)
            if (elem["dayDate"]).rstrip()=="чет" and ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                first = elem['dayTime']
                room = elem["audNum"]
                building = elem['buildNum']
                return first, room, building
            elif (elem["dayDate"]).rstrip()=="неч" and  not ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                first = elem['dayTime']
                room = elem["audNum"]
                building = elem['buildNum']
                return first, room, building
            elif (elem["dayDate"]).rstrip()=="неч/чет" and  not ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                first = elem['dayTime']
                room = elem["audNum"]
                building = elem['buildNum']
                return first, room, building
            elif (elem["dayDate"]).rstrip()=="неч/чет" and  ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                first = elem['dayTime']
                room = elem["audNum"]
                building = elem['buildNum']
                return first, room, building
            elif (elem["dayDate"]).rstrip()=="чет/неч" and  ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                first = elem['dayTime']
                room = elem["audNum"]
                building = elem['buildNum']
                return first, room, building
            elif (elem["dayDate"]).rstrip()=="чет/неч" and  not ((datetime.date(today.year, today.month, today.day).isocalendar()[1] + chetn) % 2 == 0):
                first = elem['dayTime']
                room = elem["audNum"]
                building = elem['buildNum']
                return first, room, building
            elif dateinstr != -1:
                first = elem['dayTime']
                room = elem["audNum"]
                building = elem['buildNum']
                return first, room, building
            elif not ((elem["dayDate"]).rstrip()=="чет") and not ((elem["dayDate"]).rstrip()=="неч"):
                first = "(возможно) " + str(elem['dayTime'])
                room = elem["audNum"]
                building = elem['buildNum']
                return first, room, building



        #lenght = len(response)
        #first = response[0]['dayTime']
        #room = response[0]["audNum"]
        #building = response[0]['buildNum']
        #return lenght, first, room, building
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }




keyboard = {
    "inline": True,
    "buttons": [
        [
            get_button(label="Управление рассылками", color="default", payload = {'button': 'distr'}),
            get_button(label="Расписание на сегодня", color="primary", payload = {'button': 'today'})]
        ]
            
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))


def main(request):


    distrList = []
    try:
        # if request.method != "POST":
            # return "ok"
        #print(request.headers)
        #data = json.loads(request.data)

        sql="SELECT * FROM Users WHERE groupReal > -1 AND ID_VK < 2000000000 AND distr > -1 ORDER BY Groupp"
        cursor.execute(sql)
        result = cursor.fetchall()
        #result.sort()
        #lastgroup = 0
        #print(result)
        ans = ""
        #for row in result:
        #    ans += str(row[2]) + " | " + str(row[0]) + "\n"
        #ans = sorted(result, key= attrgetter('group'))
        while (len(result) != 0 ):
            #print("/")
            users = UsersDistr()
            distrList.append(users)
            group = result[0][2]
            users.group = group
            users.realGroup = result[0][5]
            for elem in result:
                #print("")
                if elem[2] == group:
                    users.users.append(elem[0])
                    result.remove(elem)
                    result.sort()


        
    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())
        #pass

    res = ""
    #sorted(distrList, key= attrgetter('group'))
    
    for elem in distrList:
        #print(1)
        res += str(elem.group) + " | " + str(','.join(str(x) for x in elem.users)) + "\n |||||||||||||||||||||||||||||||"

        try:
            print(elem.realGroup)
            bl = [9416, 9420, 9174]
            if elem.realGroup not in bl:
                first, room, building = timetableInfo(elem.group)
                #print( ",".join(','.join(str(x) for x in elem.users)))
                vk.method("messages.send", {"user_ids": ','.join(str(x) for x in elem.users), "message": "Доброе утро, студент " + "\nПервая пара в " + (str(first)).rstrip() + " " + (str(building)).rstrip() + " зд. " + (str(room)).rstrip() + " ауд.\n На улице: " + str(Weather()) + " °C" ,"keyboard": keyboard, "random_id": random.randint(1, 2147483647)})

                res1 = str(elem.group) + " Доброе утро, студент " + "\nПервая пара в " + (str(first)).rstrip() + " " + ((str(building)).rstrip()).replace("-----------------------", ":нет:") + " зд. " + ((str(room)).rstrip()).replace("-----------------------", ":нет:") + " ауд.\n На улице: " + str(Weather()) + " °C"

                print(res1)
                res += res1
                #print(res)
        except Exception as E:
            print('Ошибка:\n', traceback.format_exc())
            print("Исключение для " + str(elem.realGroup))
            print(timetableInfo(elem.group))


    return res
