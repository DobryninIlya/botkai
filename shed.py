from apscheduler.schedulers.blocking import BlockingScheduler
from .botkai import distribution
import datetime


sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    print('This job is run every three minutes.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=10, minutes = 2)
def func()
    print("working sheduler")
    distribution.main()

sched.start()