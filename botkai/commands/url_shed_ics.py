import aiohttp

from .. import classes as command_class
from ..keyboards import keyboardicalendarGuide
from ..classes import vk
import random


async def GetDocShedule(group, id, user):
    message = "http://kaibotkai.herokuapp.com/download/shedule/?groupid={}".format(user.groupId)
    with open('{}.txt'.format(group), 'w') as f:
        f.write(str(message))
    a = await vk.docs.getMessagesUploadServer(type="doc", peer_id=id)
    async with aiohttp.ClientSession() as session:
        async with await session.post(a["upload_url"],
                                      data={"file": open(str(group) + ".txt", "rb")}) as response:
            b = await response.json()

    c = await vk.docs.save(file=b["file"])
    d = "doc" + str(c["doc"]["owner_id"]) + "_" + str(c["doc"]["id"])
    return d


async def info(MessageSettings, user):
    message = """URL ссылка на календарь позволяет добавить ваше расписание в онлайн календари, например в Outlook. 
    Такое расписание не нужно скачивать, календарь автоматически скачает его по этой ссылке.
    Просто скопируйте эту ссылку и вставьте в ваш календарь.
    (функция временно неработает)
    """
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=message,
                           keyboard=keyboardicalendarGuide,
                           random_id=random.randint(1, 2147483647))
    message = "Откройте файл и скопируйте ссылку."
    await vk.messages.send(peer_id=MessageSettings.getPeer_id(),
                           message=message,
                           attachment=await GetDocShedule(user.groupId, MessageSettings.getId(), user),
                           random_id=random.randint(1, 2147483647))


info_command = command_class.Command()

info_command.keys = ['url ссылка на календарь']
info_command.desciption = 'ссылка на календарь в Интернете для добавления в онлайн календари'
info_command.payload = "url_shed_ics"
info_command.process = info
