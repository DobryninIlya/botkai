from apscheduler.schedulers.blocking import BlockingScheduler
from botkai.distribution import main as distribution
import datetime
import requests
import json
import traceback
from botkai.classes import connection, cursor

sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=1)
def func():
    print("working sheduler")
    distribution()
    sched.shutdown()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

#@sched.scheduled_job('cron', day_of_week='mon-fri', hour=10, minute = 27)
def func():
    print("working sheduler")
    distribution()
    sched.shutdown()


BASE_URL = 'https://kai.ru/raspisanie'

@sched.scheduled_job('interval', minutes=1)
def getGroupsResponse():
    try:
        response = requests.post( BASE_URL + "?p_p_id=pubStudentSchedule_WAR_publicStudentSchedule10&p_p_lifecycle=2&p_p_resource_id=getGroupsURL", 
        headers = {'Content-Type': "application/x-www-form-urlencoded"}, 
        params = {"p_p_id":"pubStudentSchedule_WAR_publicStudentSchedule10","p_p_lifecycle":"2","p_p_resource_id":"schedule"}, timeout = 5 )
        response = response.json()
        print("INSERT INTO saved_timetable VALUES (1, {},\"{}\")".format(datetime.date.today(), response))
        cursor.execute("INSERT INTO saved_timetable VALUES (1, {},\"{}\")".format(datetime.date.today(), response))
        connection.commit()
        sched.shutdown()
    except:
        print('Ошибка:\n', traceback.format_exc())  



sched.start()