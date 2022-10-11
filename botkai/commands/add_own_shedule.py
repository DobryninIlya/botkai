import random
import aiohttp
from .. import classes as command_class
from ..classes import vk, MessageSettings


async def GetDocShedule(id):
    a = await vk.docs.getMessagesUploadServer(type="doc",
                                              peer_id=id)
    async with aiohttp.ClientSession() as session:
        async with await session.post(a["upload_url"], data={"file": open("botkai/shed_example.xlsx", "rb")}) as response:
            b = await response.json()

    c = await vk.docs.save(file=b["file"])
    d = "doc" + str(c["doc"]["owner_id"]) + "_" + str(c["doc"]["id"])
    return d


async def info():
    id = MessageSettings.getId()
    msg = "Заполните бланк расписания. Инструкции по заполнению указаны в файле (колонка справа)" \
          "Как заполните расписание - прикрепите файл к сообщению с текстом 'загрузить расписание' и отправьте его"
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=msg,
                           random_id=random.randint(1, 2147483647),
                           attachment= await GetDocShedule(id))
    return "ok"


command = command_class.Command()

command.keys = ['добавить свое расписание']
command.desciption = 'добавить свое расписание'
command.process = info
command.payload = "add_own_shedule"
