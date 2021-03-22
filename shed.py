import datetime
import json
import traceback

import requests
from apscheduler.schedulers.background import BackgroundScheduler

from botkai.classes import cursor, UserParams, vk_widget
from botkai.distribution import main as distribution
from scripts.shed_updater import shed_update

uptime = datetime.datetime.now()
sched = BackgroundScheduler()


# @sched.scheduled_job('interval', minutes=1)
# @sched.scheduled_job('cron', day_of_week='mon-sat', hour=4)
# def func():
#     distribution()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')


@sched.scheduled_job('cron', day_of_week='mon-sat', hour=4)
def func():
    distribution()
    # sched.shutdown()


BASE_URL = 'https://kai.ru/raspisanie'


# UPDATE GROUPS LIST
@sched.scheduled_job('interval', hours=2)
def getGroupsResponse():
    try:
        response = requests.post(
            BASE_URL + "?p_p_id=pubStudentSchedule_WAR_publicStudentSchedule10&p_p_lifecycle=2&p_p_resource_id=getGroupsURL",
            headers={'Content-Type': "application/x-www-form-urlencoded"},
            params={"p_p_id": "pubStudentSchedule_WAR_publicStudentSchedule10", "p_p_lifecycle": "2",
                    "p_p_resource_id": "schedule"}, timeout=60)
        response = response.json()
        if not response:
            return
        # cursor.execute("INSERT INTO saved_timetable (groupp, date_update, shedule) VALUES (1, \'{}\',\'{}\')".format(datetime.date.today(), json.dumps(response)))
        cursor.execute("UPDATE public.saved_timetable SET date_update = '{}', shedule = '{}' WHERE groupp = 1".format(
            datetime.date.today(), json.dumps(response)))
    except:
        print('Ошибка:\n', traceback.format_exc())
    return


@sched.scheduled_job('interval', hours=6)
def scheduled_job():
    shed_update()


@sched.scheduled_job('interval', minutes=1)
def widget_update():
    try:
        sql = "SELECT COUNT(ID_VK) FROM Users;"
        cursor.execute(sql)
        delta = datetime.datetime.now() - uptime
        text = "Состояние: активен\n" \
               "Пользователей сегодня: {}\n" \
               "Всего: {}\n" \
               "{}".format(UserParams.statUser, cursor.fetchone()[0], delta.strptime("%H ч. %M м."))
        code = f"""
        return {
        "title": "Состояние",
          "text" : {text}
          "more": "Написать сообщение",
          "more_url": "https://vk.me/botraspisanie",
          "descr": "Статистика использования",
    };    """
        response = vk_widget.method("appWidgets.update", {"type": "text", "code": code})
        print(response)
    except:
        print('Ошибка:\n', traceback.format_exc())



widget_update()
sched.start()
