from apscheduler.schedulers.blocking import BlockingScheduler
from botkai.distribution import main as distribution
import datetime
import requests
import json
import traceback
from botkai.classes import connection, cursor

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def func():
    print("working sheduler")
    distribution()
    sched.shutdown()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=4)
def func():
    print("working sheduler")
    distribution()
    sched.shutdown()


BASE_URL = 'https://kai.ru/raspisanie'

# UPDATE GROUPS LIST
@sched.scheduled_job('interval', hours=2)
def getGroupsResponse():
    try:
        response = requests.post( BASE_URL + "?p_p_id=pubStudentSchedule_WAR_publicStudentSchedule10&p_p_lifecycle=2&p_p_resource_id=getGroupsURL", 
        headers = {'Content-Type': "application/x-www-form-urlencoded"}, 
        params = {"p_p_id":"pubStudentSchedule_WAR_publicStudentSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"}, timeout = 60 )
        response = response.json()
        if not response:
            return
        # cursor.execute("INSERT INTO saved_timetable (groupp, date_update, shedule) VALUES (1, \'{}\',\'{}\')".format(datetime.date.today(), json.dumps(response)))
        cursor.execute("UPDATE public.saved_timetable SET date_update = '{}', shedule = '{}' WHERE groupp = 1".format(datetime.date.today(), json.dumps(response)))
    except:
        print('Ошибка:\n', traceback.format_exc())  
    return

getGroupsResponse()
sched.start()