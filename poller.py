import asyncio
from asyncio import Task
from typing import Optional
from aiovk import TokenSession
from aiovk.longpoll import BotsLongPoll, API


class Poller:
    def __init__(self, token: str, queue: asyncio.Queue):
        TokenSession.API_VERSION = '5.103'
        self.session = TokenSession(access_token=token)
        self.api = API(self.session)
        self.vk_client = BotsLongPoll(self.session, group_id=196887204)
        self.queue = queue
        self._task: Optional[Task] = None

    async def _worker(self):
        while True:
            async for event in self.vk_client.iter():
                self.queue.put_nowait(event)

    async def start(self):
        self._task = asyncio.create_task(self._worker())


    async def stop(self):
        self._task.cancel()
