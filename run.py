from vk_api.bot_longpoll import VkBotLongPoll,VkBotEventType
import vk_api
import random
import os
import traceback
from pprint import pprint
# print("OS path is ", os.getcwd())
from botkai.events.message_new import message_new
from threading import Thread

import asyncio
from aiovk import TokenSession
from aiovk.longpoll import BotsLongPoll, API
from botkai.events.message_new import message_new

TokenSession.API_VERSION = '5.103'
session = TokenSession(access_token=os.getenv("VK_TOKEN"))
api = API(session)


events = asyncio.Queue()

async def poller():
    lp = BotsLongPoll(session, group_id=196887204)

    async for event in lp.iter():
        print(event)
        try:
            if event["type"] == 'message_new':
                await events.put(event)
                # print(len(events), events)
                # await message_new(0, event)
                # delay = int(event["object"]['message']['text'])
                #
                # if delay == 1:
                #     await asyncio.sleep(delay)
                #     mesg = await api.users.get(user_ids=1)
                # else:
                #     await asyncio.sleep(delay)
                #     mesg = await api.users.get(user_ids=2)
                # print(mesg[0]['first_name'])
        except Exception as E:
            print('Ошибка:\n', traceback.format_exc())

async def answerer():
    print("answerer is working")
    # print(await events.get())
    try:
        while True:
            event = await events.get()
            if event["type"] == 'message_new':

                # await message_new(0, event)
                delay = int(event["object"]['message']['text'])

                if delay == 1:
                    await asyncio.sleep(delay)
                    mesg = await api.users.get(user_ids=1)
                else:
                    await asyncio.sleep(delay)
                    mesg = await api.users.get(user_ids=2)
                print(mesg[0]['first_name'])

    except Exception as E:
        print('Ошибка:\n', traceback.format_exc())

#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(poller())
# loop.run_until_complete(answerer())

ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(poller()), ioloop.create_task(answerer())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()
