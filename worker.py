import asyncio
import datetime
import traceback
from typing import List
from aiovk import TokenSession
from aiovk.longpoll import BotsLongPoll, API
from botkai.events.message_new import message_new

class Worker:
    def __init__(self, token: str, queue: asyncio.Queue, concurrent_workers: int):
        TokenSession.API_VERSION = '5.103'
        self.session = TokenSession(access_token=token)
        self.api = API(self.session)
        self.vk_client = BotsLongPoll(self.session, group_id=196887204)
        self.queue = queue
        self.concurrent_workers = concurrent_workers
        self._tasks: List[asyncio.Task] = []

    async def handle_update(self, event):
        print("handle update")
        try:
            if event["type"] == 'message_new':
                await message_new(0, event)

        except:
            print('Ошибка:\n', traceback.format_exc())
        # print("before", datetime.datetime.now())
        # await asyncio.sleep(10)
        # print("after", datetime.datetime.now())
        # await self.vk_client.send_message(upd.message.chat.id, upd.message.text)

    async def _worker(self):
        while True:
            upd = await self.queue.get()
            try:
                await self.handle_update(upd)
            finally:
                self.queue.task_done()

    async def start(self):
        self._tasks = [asyncio.create_task(self._worker()) for _ in range(self.concurrent_workers)]
        print("poller has been started")


    async def stop(self):
        await self.queue.join()
        for t in self._tasks:
            t.cancel()
