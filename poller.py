import asyncio
import os
import traceback
from asyncio import Task
from typing import Optional
from aiovk import TokenSession
from aiovk.longpoll import BotsLongPoll, API


class Poller:
    def __init__(self, token: str, queue: asyncio.Queue):
        TokenSession.API_VERSION = '5.130'
        self.session = TokenSession(access_token=token)
        self.api = API(self.session)
        self.vk_client = BotsLongPoll(self.session, group_id=os.getenv("VK_GROUP"), timeout=30)
        self.queue = queue
        self._task: Optional[Task] = None

    async def _worker(self):
        while True:
            try:
                async for event in self.vk_client.iter():
                    self.queue.put_nowait(event)
            except asyncio.exceptions.TimeoutError:
                print('Ошибка хэндлера timeout error:\n', traceback.format_exc(), flush=True)
                continue
            except:
                print('Ошибка хэндлера:\n', traceback.format_exc(), flush=True)

    async def start(self):
        self._task = asyncio.create_task(self._worker())

    async def stop(self):
        self._task.cancel()
