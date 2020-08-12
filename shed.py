from apscheduler.schedulers.blocking import BlockingScheduler
from botkai.distribution import main as distribution
import datetime


sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=1)
def func():
    print("working sheduler")
    distribution()
    sched.shutdown()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=10, minute = 27)
def func():
    print("working sheduler")
    distribution()
    sched.shutdown()

sched.start()